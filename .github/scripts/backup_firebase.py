"""
Firebase Backup — AESOP Academy
Exports Firestore collections to JSON and uploads to Firebase Storage.
Runs nightly via GitHub Actions.
"""

import json
import os
import sys
import datetime
import tempfile
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore, storage

# ── CONFIG ────────────────────────────────────────────────────────────────────

PROJECT_ID      = "playagame-f733d"
STORAGE_BUCKET  = "playagame-f733d.firebasestorage.app"
BACKUP_PREFIX   = "backups"
RETAIN_DAYS     = 30
COLLECTIONS     = ["learners", "examResults", "config"]

# ── INIT ──────────────────────────────────────────────────────────────────────

def init_app():
    sa_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_JSON env var not set")
    cred_dict = json.loads(sa_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {"storageBucket": STORAGE_BUCKET})

# ── EXPORT ────────────────────────────────────────────────────────────────────

def export_collection(db, collection_name):
    """Export all documents in a Firestore collection to a list of dicts."""
    docs = db.collection(collection_name).stream()
    result = {}
    count = 0
    for doc in docs:
        result[doc.id] = doc.to_dict()
        count += 1
    print(f"  {collection_name}: {count} documents")
    return result

def serialize(obj):
    """JSON-serialize Firestore types (Timestamps, etc.)."""
    if hasattr(obj, "isoformat"):          # datetime / DatetimeWithNanoseconds
        return obj.isoformat()
    if hasattr(obj, "_seconds"):           # Firestore Timestamp
        return datetime.datetime.utcfromtimestamp(obj._seconds).isoformat() + "Z"
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    return obj

# ── UPLOAD ────────────────────────────────────────────────────────────────────

def upload(bucket, blob_path, data):
    """Upload a dict as a JSON blob to Firebase Storage."""
    blob = bucket.blob(blob_path)
    blob.upload_from_string(
        json.dumps(data, indent=2, default=str),
        content_type="application/json",
    )
    print(f"  uploaded → gs://{STORAGE_BUCKET}/{blob_path}")

# ── CLEANUP ───────────────────────────────────────────────────────────────────

def cleanup_old_backups(bucket, cutoff_date):
    """Delete backup folders older than cutoff_date."""
    prefix = BACKUP_PREFIX + "/"
    blobs = bucket.list_blobs(prefix=prefix)
    deleted = 0
    for blob in blobs:
        # blob.name looks like "backups/2026-01-01/collection.json"
        parts = blob.name.split("/")
        if len(parts) < 2:
            continue
        try:
            folder_date = datetime.date.fromisoformat(parts[1])
        except ValueError:
            continue
        if folder_date < cutoff_date:
            blob.delete()
            deleted += 1
    if deleted:
        print(f"  cleaned up {deleted} blobs older than {cutoff_date}")

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    today     = datetime.date.today()
    date_str  = today.isoformat()
    cutoff    = today - datetime.timedelta(days=RETAIN_DAYS)

    print(f"=== Firebase Backup — {date_str} ===\n")

    init_app()
    db     = firestore.client()
    bucket = storage.bucket()

    print("Exporting collections...")
    manifest = {"date": date_str, "collections": {}}

    for coll in COLLECTIONS:
        try:
            data = export_collection(db, coll)
            serialized = serialize(data)
            blob_path = f"{BACKUP_PREFIX}/{date_str}/{coll}.json"
            upload(bucket, blob_path, serialized)
            manifest["collections"][coll] = len(data)
        except Exception as e:
            print(f"  ERROR exporting {coll}: {e}", file=sys.stderr)
            manifest["collections"][coll] = f"ERROR: {e}"

    # Upload manifest (quick health-check file)
    upload(bucket, f"{BACKUP_PREFIX}/{date_str}/manifest.json", manifest)

    print("\nCleaning up old backups...")
    cleanup_old_backups(bucket, cutoff)

    errors = [v for v in manifest["collections"].values() if isinstance(v, str) and v.startswith("ERROR")]
    if errors:
        print(f"\nFinished with {len(errors)} error(s).", file=sys.stderr)
        sys.exit(1)

    print(f"\nDone. Backup at gs://{STORAGE_BUCKET}/{BACKUP_PREFIX}/{date_str}/")


if __name__ == "__main__":
    main()
