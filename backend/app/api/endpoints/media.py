from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.media import MediaModel
from app.schemas.media import MediaCreate, MediaUpdate, MediaResponse, MediaAnalyzeRequest, SongRecommendationResponse
from firebase_admin import storage
from datetime import datetime, timezone
import logging
import base64
import json

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from app.core.config import settings

logger = logging.getLogger(__name__)

# Configure Gemini
if GENAI_AVAILABLE and settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

router = APIRouter()

def get_media_model():
    """Dependency to get MediaModel instance"""
    return MediaModel()

@router.get("/", response_model=List[MediaResponse])
def get_media(skip: int = 0, limit: int = 100, media_model: MediaModel = Depends(get_media_model)):
    """Get all media items with pagination"""
    media_items = media_model.get_all(limit=limit, offset=skip)
    return media_items

@router.get("/ordered/created-at", response_model=List[MediaResponse])
def get_media_ordered_by_created_at(skip: int = 0, limit: int = 100, media_model: MediaModel = Depends(get_media_model)):
    """Get all media items ordered by created_at (oldest to newest)"""
    media_items = media_model.get_all_ordered_by_created_at(limit=limit, offset=skip)
    return media_items

@router.get("/{media_id}", response_model=MediaResponse)
def get_media_item(media_id: str, media_model: MediaModel = Depends(get_media_model)):
    """Get a specific media item by ID"""
    media_item = media_model.get(media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media item not found")
    return media_item

@router.post("/", response_model=MediaResponse)
def create_media(media: MediaCreate, media_model: MediaModel = Depends(get_media_model)):
    """Create a new media item"""
    media_data = media.model_dump()

    # Fetch latest mood from database if not provided
    if "user_mood" not in media_data or not media_data.get("user_mood"):
        mood_collection = media_model.db.collection("mood")
        mood_docs = mood_collection.order_by("created_at", direction="DESCENDING").limit(1).stream()

        mood_list = list(mood_docs)
        if mood_list:
            media_data["user_mood"] = mood_list[0].to_dict().get("mood", "")
            logger.info(f"✅ Fetched latest user mood for new media: {media_data['user_mood']}")
        else:
            media_data["user_mood"] = ""
            logger.warning("⚠️ No mood found in database")

    doc_id = media_model.create(media_data)

    # Return the created media item
    created_media = media_model.get(doc_id)
    if created_media is None:
        raise HTTPException(status_code=500, detail="Failed to create media item")

    return created_media

@router.put("/{media_id}", response_model=MediaResponse)
def update_media(media_id: str, media_update: MediaUpdate, media_model: MediaModel = Depends(get_media_model)):
    """Update a media item"""
    update_data = media_update.model_dump(exclude_unset=True)

    success = media_model.update(media_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Media item not found")

    # Return the updated media item
    updated_media = media_model.get(media_id)
    return updated_media

@router.delete("/{media_id}")
def delete_media(media_id: str, media_model: MediaModel = Depends(get_media_model)):
    """Delete a media item"""
    success = media_model.delete(media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media item not found")

    return {"message": "Media item deleted successfully"}

@router.post("/analyze/{media_id}")
async def analyze_media(media_id: str, media_model: MediaModel = Depends(get_media_model)):
    """
    Fetch an image from Firebase Storage and analyze it with Gemini.
    This endpoint is called after a new image is uploaded to the bucket.
    """
    # Get media metadata from Firestore
    media_item = media_model.get(media_id)
    if media_item is None:
        raise HTTPException(status_code=404, detail="Media item not found")

    # Verify it's an image
    if media_item.get("type") != "image":
        raise HTTPException(status_code=400, detail="Media item is not an image")

    storage_url = media_item.get("storage_url")
    if not storage_url:
        raise HTTPException(status_code=400, detail="No storage URL found")

    # Download image from Firebase Storage
    try:
        # Parse the storage path from the URL
        # URL format: https://storage.googleapis.com/bucket-name/path/to/file.jpg
        bucket = storage.bucket()

        # Extract blob path from storage_url
        blob_path = storage_url.split(f"{bucket.name}/")[-1]
        blob = bucket.blob(blob_path)

        # Download image bytes
        image_bytes = blob.download_as_bytes()

        # TODO: Call Gemini API here with image_bytes
        # Example:
        # analysis_result = await analyze_with_gemini(image_bytes)
        # media_model.update(media_id, {
        #     "summary": analysis_result.get("summary"),
        #     "elements": analysis_result.get("elements"),
        #     "tags": analysis_result.get("tags")
        # })

        return {
            "message": "Image fetched successfully",
            "media_id": media_id,
            "image_size_bytes": len(image_bytes),
            "note": "TODO: Add Gemini analysis logic here"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch image: {str(e)}")

@router.post("/analyze-new")
async def analyze_new_upload(request: MediaAnalyzeRequest, media_model: MediaModel = Depends(get_media_model)):
    """
    Analyze a newly uploaded image from Firebase Storage.
    Called by Cloud Function when Raspberry Pi uploads an image.
    This endpoint:
    1. Creates a Firestore entry with the image metadata
    2. Fetches the image from storage
    3. Analyzes it with Gemini (TODO)
    """
    logger.info("=" * 80)
    logger.info("🚀 ANALYZE-NEW ENDPOINT CALLED")
    logger.info(f"📸 Storage URL: {request.storage_url}")
    logger.info(f"📝 Type: {request.type}")
    logger.info("=" * 80)

    storage_url = request.storage_url

    # Download image from Firebase Storage first (before creating Firestore entry)
    try:
        logger.info("⬇️  Downloading image from Firebase Storage...")
        bucket = storage.bucket()

        # Extract blob path from storage_url
        # URL format: https://storage.googleapis.com/bucket-name/path/to/file.jpg
        # Split on .app/ to get the path after the bucket name
        if ".firebasestorage.app/" in storage_url:
            blob_path = storage_url.split(".firebasestorage.app/")[-1]
        elif ".appspot.com/" in storage_url:
            blob_path = storage_url.split(".appspot.com/")[-1]
        else:
            # Fallback: try to extract from the URL
            blob_path = storage_url.split(f"/{bucket.name}/")[-1]

        # URL decode the blob path (to handle spaces and special characters)
        from urllib.parse import unquote
        blob_path = unquote(blob_path)

        logger.info(f"📁 Blob path: {blob_path}")

        blob = bucket.blob(blob_path)

        # Download image bytes
        image_bytes = blob.download_as_bytes()
        logger.info(f"✅ Image downloaded successfully! Size: {len(image_bytes)} bytes")

        # Call Gemini API to analyze the image
        logger.info("🤖 Analyzing image with Gemini...")

        try:
            if not GENAI_AVAILABLE:
                raise Exception("google-generativeai package not installed")

            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Prepare image for Gemini
            image_parts = [{
                'mime_type': 'image/jpeg',
                'data': base64.b64encode(image_bytes).decode('utf-8')
            }]

            # Create prompt for structured output
            prompt = """Analyze this image and provide:
1. A 1-2 sentence summary describing what's in the image
2. A list of key elements/objects visible in the image
3. The overall mood/emotion conveyed by the image (e.g., happy, calm, energetic, melancholic, peaceful, etc.)

Respond in JSON format with this structure:
{
    "summary": "your 1-2 sentence summary here",
    "elements": ["element1", "element2", "element3", ...],
    "mood": "single word or short phrase describing the mood"
}"""

            # Generate content
            response = model.generate_content([prompt, image_parts[0]])

            # Parse JSON response (handle markdown code blocks if present)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif response_text.startswith('```'):
                response_text = response_text.split('```')[1].split('```')[0].strip()

            analysis_result = json.loads(response_text)

            logger.info(f"✅ Gemini analysis complete!")
            logger.info(f"📝 Summary: {analysis_result.get('summary')}")
            logger.info(f"🏷️  Elements: {analysis_result.get('elements')}")
            logger.info(f"😊 Mood: {analysis_result.get('mood')}")

            # Get current timestamp for processing time
            processed_at = datetime.now(timezone.utc)

            # Fetch latest mood from database
            logger.info("😊 Fetching latest user mood from database...")
            mood_collection = media_model.db.collection("mood")
            mood_docs = mood_collection.order_by("created_at", direction="DESCENDING").limit(1).stream()

            user_mood = ""
            mood_list = list(mood_docs)
            if mood_list:
                user_mood = mood_list[0].to_dict().get("mood", "")
                logger.info(f"✅ User Mood (from database): {user_mood}")
            else:
                logger.warning("⚠️ No mood found in database")
                user_mood = ""

            # Now create Firestore entry with all data (analysis complete)
            logger.info("📊 Creating Firestore entry with analysis results...")
            media_data = {
                "type": request.type,
                "storage_url": storage_url,
                "ts": datetime.now(timezone.utc),
                "summary": analysis_result.get("summary"),
                "elements": analysis_result.get("elements"),
                "mood": analysis_result.get("mood"),
                "user_mood": user_mood,
                "processed_at": processed_at
            }

            doc_id = media_model.create(media_data)

            if not doc_id:
                logger.error("❌ Failed to create Firestore entry")
                raise HTTPException(status_code=500, detail="Failed to create media entry")

            logger.info(f"✅ Firestore entry created with ID: {doc_id}")

        except Exception as gemini_error:
            logger.error(f"❌ Gemini analysis failed: {str(gemini_error)}")
            # Create Firestore entry even if analysis fails
            media_data = {
                "type": request.type,
                "storage_url": storage_url,
                "ts": datetime.now(timezone.utc),
                "error": str(gemini_error)
            }
            doc_id = media_model.create(media_data)
            analysis_result = {
                "summary": "Analysis failed",
                "elements": [],
                "mood": None,
                "error": str(gemini_error)
            }
            processed_at = None

        logger.info("=" * 80)

        return {
            "message": "Image analyzed successfully",
            "media_id": doc_id,
            "storage_url": storage_url,
            "image_size_bytes": len(image_bytes),
            "analysis": {
                "summary": analysis_result.get("summary"),
                "elements": analysis_result.get("elements"),
                "mood": analysis_result.get("mood"),
                "processed_at": processed_at.isoformat() if 'processed_at' in locals() else None
            }
        }

    except Exception as e:
        logger.error(f"❌ Error downloading/processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")

@router.post("/recommend-song", response_model=SongRecommendationResponse)
async def recommend_song(media_id: str, media_model: MediaModel = Depends(get_media_model)):
    """
    Recommend a song based on media analysis and user questionnaire.
    Called by Cloud Function when a new media entry is created in Firestore.

    Args:
        media_id: The ID of the media document in Firestore
    """
    from app.models.questionnaire import QuestionnaireModel
    from app.utils.spotify import search_track

    logger.info("=" * 80)
    logger.info("🎵 RECOMMEND-SONG ENDPOINT CALLED")
    logger.info(f"📋 Media ID: {media_id}")
    logger.info("=" * 80)

    # Fetch media data from Firestore
    media_item = media_model.get(media_id)

    if not media_item:
        logger.error(f"❌ Media item not found: {media_id}")
        raise HTTPException(status_code=404, detail="Media item not found")

    # Extract image analysis data
    image_mood = media_item.get("mood")
    image_summary = media_item.get("summary")
    image_elements = media_item.get("elements", [])

    logger.info(f"🖼️  Image Mood: {image_mood}")
    logger.info(f"📝 Image Summary: {image_summary}")
    logger.info(f"🏷️  Image Elements: {image_elements}")

    # Fetch latest questionnaire
    questionnaire_model = QuestionnaireModel()
    questionnaires = questionnaire_model.get_all(limit=1)

    questionnaire_data = None
    if questionnaires:
        questionnaire_data = questionnaires[0].get("qa_pairs", [])
        logger.info(f"📋 Found questionnaire with {len(questionnaire_data)} QA pairs")
    else:
        logger.warning("⚠️  No questionnaire found")

    # Fetch latest mood from database
    mood_collection = media_model.db.collection("mood")
    mood_docs = mood_collection.order_by("created_at", direction="DESCENDING").limit(1).stream()

    user_mood = ""
    mood_list = list(mood_docs)
    if mood_list:
        user_mood = mood_list[0].to_dict().get("mood", "")
        logger.info(f"😔 User Mood (from database): {user_mood}")
    else:
        logger.warning("⚠️ No mood found in database")
        user_mood = ""

    # Call Gemini to recommend a song
    try:
        if not GENAI_AVAILABLE:
            raise Exception("google-generativeai package not installed")

        logger.info("🤖 Calling Gemini for song recommendation...")

        model = genai.GenerativeModel('gemini-flash-latest')

        # Build the prompt with all context
        questionnaire_str = ""
        if questionnaire_data:
            questionnaire_str = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in questionnaire_data])

        prompt = f"""You are a music recommendation expert. Based on the following information, recommend ONE song that would be perfect for this moment.

USER PREFERENCES (from questionnaire):
{questionnaire_str if questionnaire_str else "No questionnaire data available"}

USER'S CURRENT MOOD: {user_mood}

IMAGE CONTEXT:
- Image Mood: {image_mood}
- Image Summary: {image_summary}
- Elements in Image: {', '.join(image_elements) if image_elements else 'None'}

Based on all this context, recommend a single song available on Spotify that would resonate with the user right now. The name of the song must be the same name that is available on Spotify.

Respond in JSON format with this exact structure:
{{
    "name": "Song Title",
    "artist": "Artist Name"
}}"""

        response = model.generate_content(prompt)

        # Parse JSON response
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif response_text.startswith('```'):
            response_text = response_text.split('```')[1].split('```')[0].strip()

        song_recommendation = json.loads(response_text)

        logger.info(f"✅ Song Recommendation: {song_recommendation.get('name')} by {song_recommendation.get('artist')}")

        # Search for the song on Spotify
        logger.info("🎧 Searching Spotify for the recommended song...")
        spotify_data = search_track(
            song_name=song_recommendation.get("name"),
            artist_name=song_recommendation.get("artist")
        )

        # Update media object with song data and user mood
        if spotify_data:
            logger.info(f"💾 Updating media object with Spotify data...")
            update_data = {
                "song": spotify_data.get("song"),
                "song_artist": spotify_data.get("song_artist"),
                "embed": spotify_data.get("embed"),
                "user_mood": user_mood
            }
            media_model.update(media_id, update_data)
            logger.info(f"✅ Media object updated with song: {spotify_data.get('song')}")
        else:
            logger.warning(f"⚠️ No Spotify data found for query: '{song_recommendation.get('name')}' by '{song_recommendation.get('artist')}', media object not updated")

        logger.info("=" * 80)

        return {
            "message": "Song recommended successfully",
            "media_id": media_id,
            "recommendation": {
                "name": song_recommendation.get("name"),
                "artist": song_recommendation.get("artist")
            },
            "context": {
                "user_mood": user_mood,
                "image_mood": image_mood,
                "image_summary": image_summary,
                "image_elements": image_elements,
                "questionnaire_available": bool(questionnaire_data)
            },
            "spotify": spotify_data if spotify_data else None
        }

    except Exception as e:
        logger.error(f"❌ Song recommendation failed: {str(e)}")
        logger.info("=" * 80)
        raise HTTPException(status_code=500, detail=f"Failed to recommend song: {str(e)}")