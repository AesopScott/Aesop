#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check what scheduler secrets are already in Firebase."""

import json
import sys
from pathlib import Path
import os

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("Installing firebase-admin...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "firebase-admin"])
    import firebase_admin
    from firebase_admin import credentials, firestore

# Path to the Firebase service account
appdata = os.getenv('APPDATA')
SA_PATH = Path(appdata) / ".claude/polaris/firebase-keys/playagame-f733d-firebase-adminsdk-fbsvc-5f34b68387.json"

if not SA_PATH.exists():
    print(f"ERROR: Firebase service account not found at {SA_PATH}")
    sys.exit(1)

print(f"Using service account: {SA_PATH}")

# Initialize Firebase
try:
    cred = credentials.Certificate(str(SA_PATH))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("[OK] Connected to Firebase")
except Exception as e:
    print(f"ERROR: Failed to connect to Firebase: {e}")
    sys.exit(1)

# Check for existing config
print("\n=== EXISTING CONFIG IN FIRESTORE ===\n")

try:
    # Check config collection
    config_docs = db.collection("config").stream()
    found_any = False

    for doc in config_docs:
        found_any = True
        print(f"Document: {doc.id}")
        data = doc.to_dict()
        for key, value in data.items():
            if key in ["password", "secret", "key"]:
                print(f"  {key}: [HIDDEN]")  # Hide sensitive values
            else:
                print(f"  {key}: {value}")
        print()

    if not found_any:
        print("(No documents found in config collection)")

    # Check for scheduler-specific config
    print("\n=== CHECKING FOR SCHEDULER CONFIG ===\n")

    scheduler_doc = db.collection("config").document("scheduler").get()
    if scheduler_doc.exists:
        print("[FOUND] config/scheduler")
        print(json.dumps(scheduler_doc.to_dict(), indent=2))
    else:
        print("[NOT FOUND] config/scheduler (needs to be created)")

    print("\n=== CHECKING FOR DATABASE CONFIG ===\n")

    db_doc = db.collection("config").document("database").get()
    if db_doc.exists:
        print("[FOUND] config/database")
        data = db_doc.to_dict()
        for key, value in data.items():
            if "password" in key.lower():
                print(f"  {key}: [HIDDEN]")
            else:
                print(f"  {key}: {value}")
    else:
        print("[NOT FOUND] config/database")

except Exception as e:
    print(f"ERROR reading Firebase: {e}")
    sys.exit(1)

print("\n=== NEXT STEPS ===")
print("If config/scheduler or config/database don't exist, we need to create them.")
print("You'll need to provide:")
print("  - AESOP_AZURE_CLIENT_SECRET")
print("  - AESOP_SECOND_CALENDAR_ICS")
print("  - AESOP_DB_HOST, AESOP_DB_NAME, AESOP_DB_USER, AESOP_DB_PASS")
