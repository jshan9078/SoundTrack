import os
import logging
import random
import tempfile
from typing import List
from PIL import Image
import requests
from io import BytesIO
import numpy as np

# Fix for Pillow/moviepy compatibility
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

logger = logging.getLogger(__name__)

# Ken Burns style motion effects (all images get continuous motion)
MOTION_EFFECTS = [
    'zoom_and_pan_right',
    'zoom_and_pan_left',
    'zoom_and_pan_down',
    'zoom_and_pan_up',
    'slow_zoom_in',
    'slow_zoom_out',
    'diagonal_drift_1',
    'diagonal_drift_2'
]

def ease_in_out(t):
    """Smooth easing function for natural motion"""
    return t * t * (3 - 2 * t)

def apply_motion_effect(clip, effect_type: str, duration: float):
    """Apply continuous Ken Burns style motion effects to make images feel alive"""
    w, h = clip.size

    if effect_type == 'zoom_and_pan_right':
        # Zoom in while panning right
        return clip.resize(lambda t: 1 + 0.15 * ease_in_out(t / duration)).set_position(
            lambda t: (-(w * 0.1) * ease_in_out(t / duration), 'center')
        )

    elif effect_type == 'zoom_and_pan_left':
        # Zoom in while panning left
        return clip.resize(lambda t: 1 + 0.15 * ease_in_out(t / duration)).set_position(
            lambda t: ((w * 0.1) * ease_in_out(t / duration), 'center')
        )

    elif effect_type == 'zoom_and_pan_down':
        # Zoom in while panning down
        return clip.resize(lambda t: 1 + 0.15 * ease_in_out(t / duration)).set_position(
            lambda t: ('center', -(h * 0.1) * ease_in_out(t / duration))
        )

    elif effect_type == 'zoom_and_pan_up':
        # Zoom in while panning up
        return clip.resize(lambda t: 1 + 0.15 * ease_in_out(t / duration)).set_position(
            lambda t: ('center', (h * 0.1) * ease_in_out(t / duration))
        )

    elif effect_type == 'slow_zoom_in':
        # Subtle continuous zoom in
        return clip.resize(lambda t: 1 + 0.2 * ease_in_out(t / duration))

    elif effect_type == 'slow_zoom_out':
        # Start zoomed, zoom out
        return clip.resize(lambda t: 1.2 - 0.2 * ease_in_out(t / duration))

    elif effect_type == 'diagonal_drift_1':
        # Drift diagonally top-left to bottom-right
        return clip.resize(1.15).set_position(
            lambda t: (
                -(w * 0.075) * ease_in_out(t / duration),
                -(h * 0.075) * ease_in_out(t / duration)
            )
        )

    elif effect_type == 'diagonal_drift_2':
        # Drift diagonally top-right to bottom-left
        return clip.resize(1.15).set_position(
            lambda t: (
                (w * 0.075) * ease_in_out(t / duration),
                -(h * 0.075) * ease_in_out(t / duration)
            )
        )

    else:
        # Default: subtle zoom in
        return clip.resize(lambda t: 1 + 0.1 * ease_in_out(t / duration))


def resize_and_fit_image(image_path: str, target_size: tuple) -> str:
    """
    Resize image to fit within target size while maintaining aspect ratio.
    Creates a black background canvas and centers the image (letterbox/pillarbox).
    """
    try:
        img = Image.open(image_path)

        # Convert RGBA to RGB (remove transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (0, 0, 0))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        img_width, img_height = img.size
        target_width, target_height = target_size

        # Calculate aspect ratios
        img_aspect = img_width / img_height
        target_aspect = target_width / target_height

        # Resize to fit within bounds (contain, not cover)
        if img_aspect > target_aspect:
            # Image is wider - fit to width
            new_width = target_width
            new_height = int(target_width / img_aspect)
        else:
            # Image is taller - fit to height
            new_height = target_height
            new_width = int(target_height * img_aspect)

        # Resize image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Create black canvas and paste image in center
        canvas = Image.new('RGB', target_size, (0, 0, 0))
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        canvas.paste(img, (paste_x, paste_y))

        # Save the processed image as JPEG
        canvas.save(image_path, 'JPEG', quality=95)
        logger.info(f"✂️  Resized and fitted image to {target_width}x{target_height}")
        return image_path

    except Exception as e:
        logger.error(f"Failed to resize/fit image: {str(e)}")
        return image_path

def download_image(url: str, output_path: str) -> bool:
    """Download image from URL to local path"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        logger.error(f"Failed to download image from {url}: {str(e)}")
        return False

def create_video_from_images(
    image_urls: List[str],
    audio_path: str,
    output_path: str,
    duration_per_image: float = 2.0,
    transition_duration: float = 0.5,
    video_size: tuple = (1920, 1080)  # Standard 1080p HD
) -> bool:
    """
    Create a video from a list of image URLs with transitions and audio

    Args:
        image_urls: List of image URLs
        audio_path: Path to audio file
        output_path: Path to save the output video
        duration_per_image: Duration each image is displayed (seconds)
        transition_duration: Duration of transition effects (seconds)
        video_size: Size of output video (width, height)

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"🎬 Creating video from {len(image_urls)} images at {video_size[0]}x{video_size[1]}")

        # Create temp directory for downloaded images
        temp_dir = tempfile.mkdtemp()

        # Download all images and resize/fit them
        image_paths = []
        for i, url in enumerate(image_urls):
            img_path = os.path.join(temp_dir, f"image_{i}.jpg")
            if download_image(url, img_path):
                # Resize and fit to video size (no stretching)
                resize_and_fit_image(img_path, video_size)
                image_paths.append(img_path)
            else:
                logger.warning(f"⚠️ Skipping image {i} due to download failure")

        if not image_paths:
            logger.error("❌ No images were downloaded successfully")
            return False

        logger.info(f"✅ Downloaded and processed {len(image_paths)} images")

        # Create video clips from images with continuous Ken Burns motion
        clips = []

        # Use smooth crossfade transitions
        smooth_transition = 0.8

        for i, img_path in enumerate(image_paths):
            # Create image clip
            clip = ImageClip(img_path, duration=duration_per_image)

            # Randomly select a Ken Burns motion effect for this clip
            motion_type = random.choice(MOTION_EFFECTS)

            # Apply continuous motion effect to the clip
            clip = apply_motion_effect(clip, motion_type, duration_per_image)

            logger.info(f"🎨 Image {i}: '{motion_type}' motion | crossfade")

            # Fade in first image, fade out all images
            if i == 0:
                clip = clip.fadein(smooth_transition)
            clip = clip.fadeout(smooth_transition)

            clips.append(clip)

        # Concatenate all clips with crossfade
        logger.info("🔗 Building video with crossfade transitions...")
        final_video = concatenate_videoclips(clips, method="compose", padding=-smooth_transition)

        # Add audio
        logger.info("🎵 Adding audio to video...")
        audio_clip = AudioFileClip(audio_path)

        # If audio is longer than video, trim it
        if audio_clip.duration > final_video.duration:
            audio_clip = audio_clip.subclip(0, final_video.duration)
        # If video is longer than audio, loop the audio
        elif final_video.duration > audio_clip.duration:
            # Loop audio to match video duration
            loops_needed = int(final_video.duration / audio_clip.duration) + 1
            audio_clip = audio_clip.loop(n=loops_needed).subclip(0, final_video.duration)

        final_video = final_video.set_audio(audio_clip)

        # Write output video
        logger.info(f"💾 Writing video to {output_path}...")
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=os.path.join(temp_dir, 'temp_audio.m4a'),
            remove_temp=True
        )

        # Cleanup
        for clip in clips:
            clip.close()
        audio_clip.close()
        final_video.close()

        # Remove temp images
        for img_path in image_paths:
            try:
                os.remove(img_path)
            except:
                pass

        try:
            os.rmdir(temp_dir)
        except:
            pass

        logger.info(f"✅ Video created successfully: {output_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to create video: {str(e)}")
        return False
