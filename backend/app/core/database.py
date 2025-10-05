import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings
from typing import Optional
import json
import os

# Global Firestore client
db: Optional[firestore.Client] = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global db

    if not firebase_admin._apps:
        # Check if credentials are in environment variable (for Railway)
        firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")

        if firebase_creds_json:
            # Load credentials from environment variable
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'projectId': settings.FIREBASE_PROJECT_ID,
                'storageBucket': settings.STORAGE_BUCKET
            })
        elif settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            # Use service account credentials file (for local development)
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'projectId': settings.FIREBASE_PROJECT_ID,
                'storageBucket': settings.STORAGE_BUCKET
            })
        else:
            raise Exception("Firebase credentials not found. Set FIREBASE_CREDENTIALS env var or provide credentials file.")

    db = firestore.client()
    return db

def get_db():
    """Get Firestore database client"""
    global db
    if db is None:
        db = initialize_firebase()
    return db