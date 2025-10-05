from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

class BiometricModel:
    """Firestore Biometric document model"""

    COLLECTION_NAME = "biometrics"

    def __init__(self):
        self.db = get_db()
        self.collection = self.db.collection(self.COLLECTION_NAME)

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all biometric documents ordered by createdAt (oldest to newest)"""
        query = self.collection.order_by("createdAt", direction="ASCENDING")

        if offset > 0:
            query = query.offset(offset)

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)

        return results
