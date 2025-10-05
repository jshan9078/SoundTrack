from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import media, moods, questionnaire
from app.core.config import settings
from app.core.database import initialize_firebase

app = FastAPI(
    title="SoundTrack API",
    description="Backend API for SoundTrack - A soundtrack to your life",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    initialize_firebase()

# Include routers
app.include_router(media.router, prefix="/api/media", tags=["media"])
app.include_router(moods.router, prefix="/api/moods", tags=["moods"])
app.include_router(questionnaire.router, prefix="/api/questionnaire", tags=["questionnaire"])

@app.get("/")
async def root():
    return {"message": "SoundTrack API is running with Firebase!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "firebase"}