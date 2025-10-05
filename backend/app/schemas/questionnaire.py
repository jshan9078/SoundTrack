from pydantic import BaseModel
from typing import List
from datetime import datetime

class QAPair(BaseModel):
    question: str
    answer: str

class QuestionnaireCreate(BaseModel):
    qa_pairs: List[QAPair]

class QuestionnaireResponse(BaseModel):
    id: str
    qa_pairs: List[QAPair]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
