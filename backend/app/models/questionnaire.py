from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4
from app.core.database import get_db

class QuestionnaireModel:
    """Firestore Questionnaire document model"""

    COLLECTION_NAME = "questionnaire"

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.collection(self.COLLECTION_NAME)

    def to_dict(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert questionnaire data to Firestore document format"""
        return {
            "qa_pairs": questionnaire_data.get("qa_pairs", []),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def create(self, questionnaire_data: Dict[str, Any]) -> str:
        """Create a new questionnaire document"""
        doc_id = str(uuid4())
        doc_data = self.to_dict(questionnaire_data)
        self.collection.document(doc_id).set(doc_data)
        return doc_id

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a questionnaire document by ID"""
        doc = self.collection.document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all questionnaire documents with pagination"""
        query = self.collection.order_by("created_at", direction="desc")

        if offset > 0:
            query = query.offset(offset)

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)

        return results
