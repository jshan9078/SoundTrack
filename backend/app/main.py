from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import media, moods, questionnaire, biometric, video
from app.core.config import settings
from app.core.database import initialize_firebase

app = FastAPI(
    title="SoundTrack API",
    description="Backend API for SoundTrack - A soundtrack to your life",
    version="1.0.0"
)

# Set up CORS - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    import logging
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting SoundTrack API...")
    logger.info(f"✅ CORS enabled with allow_origins=['*']")
    initialize_firebase()
    logger.info("✅ Firebase initialized")

# Include routers
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(moods.router, prefix="/api/moods", tags=["moods"])
app.include_router(questionnaire.router, prefix="/api/questionnaire", tags=["questionnaire"])
app.include_router(biometric.router, prefix="/api/biometric", tags=["biometric"])
app.include_router(video.router, prefix="/api/video", tags=["video"])

@app.get("/")
async def root():
    return {"message": "SoundTrack API is running with Firebase!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "firebase"}