from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4
from app.core.database import get_db

class MediaModel:
    """Firestore Media document model"""

    COLLECTION_NAME = "media"

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.collection(self.COLLECTION_NAME)

    def to_dict(self, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert media data to Firestore document format"""
        return {
            "session_id": media_data.get("session_id"),
            "ts": media_data.get("ts", datetime.utcnow()),
            "type": media_data.get("type"),  # 'image' or 'clip'
            "storage_url": media_data.get("storage_url"),
            "thumb_url": media_data.get("thumb_url"),
            "duration_sec": media_data.get("duration_sec"),
            "summary": media_data.get("summary"),
            "elements": media_data.get("elements", []),  # ["trees","book"]
            "tags": media_data.get("tags", []),          # ["nature","study"]
            "mood": media_data.get("mood"),
            "processed_at": media_data.get("processed_at"),
            "error": media_data.get("error"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def create(self, media_data: Dict[str, Any]) -> str:
        """Create a new media document"""
        doc_id = str(uuid4())
        doc_data = self.to_dict(media_data)
        self.collection.document(doc_id).set(doc_data)
        return doc_id

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a media document by ID"""
        doc = self.collection.document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all media documents with pagination"""
        query = self.collection.order_by("ts", direction="desc")

        if offset > 0:
            # For pagination, we'd need to implement cursor-based pagination
            # This is a simplified version
            query = query.offset(offset)

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)

        return results

    def update(self, doc_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a media document"""
        doc_ref = self.collection.document(doc_id)

        # Check if document exists
        if not doc_ref.get().exists:
            return False

        # Add updated_at timestamp
        update_data['updated_at'] = datetime.utcnow()

        doc_ref.update(update_data)
        return True

    def delete(self, doc_id: str) -> bool:
        """Delete a media document"""
        doc_ref = self.collection.document(doc_id)

        # Check if document exists
        if not doc_ref.get().exists:
            return False

        doc_ref.delete()
        return True

    def get_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all media for a specific session"""
        docs = self.collection.where("session_id", "==", session_id).order_by("ts").stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)

        return results