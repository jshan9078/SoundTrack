import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings
from typing import Optional

# Global Firestore client
db: Optional[firestore.Client] = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global db

    if not firebase_admin._apps:
        if settings.FIREBASE_CREDENTIALS_PATH:
            # Use service account credentials
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'projectId': settings.FIREBASE_PROJECT_ID,
                'storageBucket': settings.STORAGE_BUCKET
            })
        else:
            # Use default credentials (for development)
            firebase_admin.initialize_app()

    db = firestore.client()
    return db

def get_db():
    """Get Firestore database client"""
    global db
    if db is None:
        db = initialize_firebase()
    return db