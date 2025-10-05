from fastapi import APIRouter, Depends
from typing import List
from app.models.biometric import BiometricModel
from app.schemas.biometric import BiometricResponse

router = APIRouter()

def get_biometric_model():
    """Dependency to get BiometricModel instance"""
    return BiometricModel()

@router.get("/", response_model=List[BiometricResponse])
def get_biometrics(skip: int = 0, limit: int = 1000, biometric_model: BiometricModel = Depends(get_biometric_model)):
    """Get all biometric data ordered by created_at (oldest to newest)"""
    biometric_data = biometric_model.get_all(limit=limit, offset=skip)
    return biometric_data
