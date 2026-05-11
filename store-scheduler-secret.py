import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os
import json

appdata = os.getenv('APPDATA')
sa_path = Path(appdata) / ".claude/polaris/firebase-keys/playagame-f733d-firebase-adminsdk-fbsvc-5f34b68387.json"

cred = credentials.Certificate(str(sa_path))
firebase_admin.initialize_app(cred)
db = firestore.client()

scheduler_config = {
    'AESOP_AZURE_CLIENT_SECRET': 'TXW8Q~pI_Zh3mPiH~RjExkXdCzOdXEShWVSJkcMI',
    'AESOP_AZURE_CLIENT_ID': '9362894e-cca3-48d5-99f6-b135c6090cb4',
    'AESOP_AZURE_TENANT_ID': 'e6af4d4f-7ea3-4182-9d21-b6697a4abaf3',
    'AESOP_OWNER_EMAIL': 'scott@aesopacademy.org',
    'AESOP_OWNER_NAME': 'Scott',
    'updated_at': firestore.SERVER_TIMESTAMP,
}

db.collection('config').document('scheduler').set(scheduler_config, merge=True)
print("[OK] Stored scheduler config in Firebase")
