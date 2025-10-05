from fastapi import APIRouter, HTTPException, Depends
from app.schemas.video import VideoGenerateRequest, VideoGenerateResponse
from app.models.media import MediaModel
from app.utils.lyria import generate_music
from app.utils.video_generator import create_video_from_images
from firebase_admin import storage
import logging
import os
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

def get_media_model():
    """Dependency to get MediaModel instance"""
    return MediaModel()

@router.post("/generate", response_model=VideoGenerateResponse)
async def generate_video(request: VideoGenerateRequest, media_model: MediaModel = Depends(get_media_model)):
    """
    Generate a video from a list of media IDs with AI-generated music.
    Each image is displayed for 2 seconds with transitions.
    """
    logger.info("=" * 80)
    logger.info("🎬 VIDEO GENERATION ENDPOINT CALLED")
    logger.info(f"📋 Media IDs: {request.media_ids}")
    logger.info(f"🎵 Music Prompt: {request.music_prompt}")
    logger.info("=" * 80)

    try:
        # Fetch media items and get their storage URLs
        logger.info(f"🔍 Fetching media items for {len(request.media_ids)} IDs...")
        image_urls = []
        for media_id in request.media_ids:
            try:
                logger.info(f"  📄 Fetching media ID: {media_id}")
                media_item = media_model.get(media_id)
                if not media_item:
                    logger.warning(f"  ⚠️ Media item not found: {media_id}")
                    continue

                if media_item.get("type") != "image":
                    logger.warning(f"  ⚠️ Media item is not an image: {media_id} (type: {media_item.get('type')})")
                    continue

                storage_url = media_item.get("storage_url")
                if storage_url:
                    image_urls.append(storage_url)
                    logger.info(f"  ✅ Got storage URL for {media_id}")
                else:
                    logger.warning(f"  ⚠️ No storage URL for media: {media_id}")
            except Exception as e:
                logger.error(f"  ❌ Error fetching media {media_id}: {str(e)}", exc_info=True)
                continue

        if not image_urls:
            logger.error("❌ No valid images found from provided media IDs")
            raise HTTPException(status_code=400, detail="No valid images found from provided media IDs")

        logger.info(f"✅ Found {len(image_urls)} valid images")

        # Generate music with Lyria
        try:
            logger.info("🎵 Generating music with Lyria...")
            logger.info(f"  Prompt: {request.music_prompt}")
            logger.info(f"  Negative prompt: {request.negative_prompt}")
            temp_audio_path = os.path.join(tempfile.gettempdir(), "generated_music.wav")
            logger.info(f"  Temp audio path: {temp_audio_path}")

            audio_path = generate_music(
                prompt=request.music_prompt,
                negative_prompt=request.negative_prompt,
                sample_count=1,
                output_path=temp_audio_path
            )

            if not audio_path:
                logger.error("❌ Failed to generate music - generate_music returned None")
                raise HTTPException(status_code=500, detail="Failed to generate music")

            logger.info(f"✅ Music generated: {audio_path}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Music generation exception: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to generate music: {str(e)}")

        # Create video
        try:
            logger.info("🎬 Creating video from images...")
            logger.info(f"  Number of images: {len(image_urls)}")
            temp_video_path = os.path.join(tempfile.gettempdir(), "generated_video.mp4")
            logger.info(f"  Temp video path: {temp_video_path}")

            success = create_video_from_images(
                image_urls=image_urls,
                audio_path=audio_path,
                output_path=temp_video_path,
                duration_per_image=2.0,
                transition_duration=0.5
            )

            if not success:
                logger.error("❌ Failed to create video - create_video_from_images returned False")
                raise HTTPException(status_code=500, detail="Failed to create video")

            logger.info(f"✅ Video created: {temp_video_path}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Video creation exception: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to create video: {str(e)}")

        # Upload video to Firebase Storage in videos folder
        try:
            logger.info("☁️ Uploading video to Firebase Storage...")
            bucket = storage.bucket()
            logger.info(f"  Bucket: {bucket.name}")

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            blob_path = f"videos/video_{timestamp}.mp4"
            logger.info(f"  Blob path: {blob_path}")

            blob = bucket.blob(blob_path)

            # Upload file
            logger.info(f"  Uploading file from: {temp_video_path}")
            blob.upload_from_filename(temp_video_path, content_type='video/mp4')
            logger.info("  ✅ File uploaded")

            # Make the blob publicly accessible
            blob.make_public()
            logger.info("  ✅ Blob made public")

            video_url = blob.public_url
            logger.info(f"✅ Video uploaded to: {video_url}")
        except Exception as e:
            logger.error(f"❌ Firebase upload exception: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to upload video to Firebase: {str(e)}")

        # Cleanup temp files
        try:
            logger.info("🧹 Cleaning up temp files...")
            os.remove(temp_audio_path)
            os.remove(temp_video_path)
            logger.info("  ✅ Temp files removed")
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to cleanup temp files: {str(e)}")

        logger.info("=" * 80)

        return {
            "message": "Video generated successfully",
            "video_url": video_url,
            "media_ids": request.media_ids
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Video generation failed with unexpected error: {str(e)}", exc_info=True)
        logger.info("=" * 80)
        raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")

