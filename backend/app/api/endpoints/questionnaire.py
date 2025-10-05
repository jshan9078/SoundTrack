from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.questionnaire import QuestionnaireModel
from app.schemas.questionnaire import QuestionnaireCreate, QuestionnaireResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_questionnaire_model():
    """Dependency to get QuestionnaireModel instance"""
    return QuestionnaireModel()

@router.post("/", response_model=QuestionnaireResponse)
async def create_questionnaire(
    questionnaire: QuestionnaireCreate,
    questionnaire_model: QuestionnaireModel = Depends(get_questionnaire_model)
):
    """
    Create a new questionnaire with question-answer pairs.

    Example request body:
    {
        "qa_pairs": [
            {"question": "What is your name?", "answer": "John"},
            {"question": "What is your favorite color?", "answer": "Blue"}
        ]
    }
    """
    logger.info("=" * 80)
    logger.info("📋 CREATE QUESTIONNAIRE ENDPOINT CALLED")
    logger.info(f"Number of QA pairs: {len(questionnaire.qa_pairs)}")
    logger.info("=" * 80)

    # Convert to dict for storage
    questionnaire_data = {
        "qa_pairs": [qa.model_dump() for qa in questionnaire.qa_pairs]
    }

    # Create in Firestore
    doc_id = questionnaire_model.create(questionnaire_data)

    if not doc_id:
        logger.error("❌ Failed to create questionnaire")
        raise HTTPException(status_code=500, detail="Failed to create questionnaire")

    logger.info(f"✅ Questionnaire created with ID: {doc_id}")
    logger.info("=" * 80)

    # Return the created questionnaire
    created_questionnaire = questionnaire_model.get(doc_id)
    if created_questionnaire is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve created questionnaire")

    return created_questionnaire

@router.get("/", response_model=List[QuestionnaireResponse])
async def get_questionnaires(
    skip: int = 0,
    limit: int = 100,
    questionnaire_model: QuestionnaireModel = Depends(get_questionnaire_model)
):
    """Get all questionnaires with pagination"""
    questionnaires = questionnaire_model.get_all(limit=limit, offset=skip)
    return questionnaires

@router.get("/{questionnaire_id}", response_model=QuestionnaireResponse)
async def get_questionnaire(
    questionnaire_id: str,
    questionnaire_model: QuestionnaireModel = Depends(get_questionnaire_model)
):
    """Get a specific questionnaire by ID"""
    questionnaire = questionnaire_model.get(questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire
