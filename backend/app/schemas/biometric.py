from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class BiometricResponse(BaseModel):
    id: str
    createdAt: datetime
    timestamp: Optional[datetime] = None
    sessionId: Optional[str] = None
    eegData: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        extra = "allow"  # Allow additional fields from Firestore
