import base64
import os
import logging
import json
from typing import Optional
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)

def get_google_access_token() -> str:
    """Get Google Cloud access token using Firebase service account credentials"""
    # Try to get credentials from environment variable first
    firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")

    if firebase_creds_json:
        cred_dict = json.loads(firebase_creds_json)
        credentials = service_account.Credentials.from_service_account_info(
            cred_dict,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    elif settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        credentials = service_account.Credentials.from_service_account_file(
            settings.FIREBASE_CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
    else:
        raise Exception("Firebase credentials not found")

    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token

def generate_music(prompt: str, negative_prompt: str = "", sample_count: int = 1, output_path: str = None) -> Optional[str]:
    """
    Generate music using Google Lyria API

    Args:
        prompt: Music generation prompt
        negative_prompt: What to avoid in the music
        sample_count: Number of samples to generate (we'll use the first one)
        output_path: Path to save the generated audio file

    Returns:
        Path to the generated audio file or None if failed
    """
    try:
        # Get access token
        access_token = get_google_access_token()

        # Lyria API endpoint
        project_id = settings.FIREBASE_PROJECT_ID
        api_endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/lyria-002:predict"

        # Prepare request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        data = {
            "instances": [{
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "sample_count": sample_count
            }],
            "parameters": {}
        }

        logger.info(f"🎵 Generating music with Lyria API: '{prompt}'")

        # Make API request
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Extract audio from response
        predictions = result.get("predictions", [])
        if not predictions:
            logger.error("❌ No predictions returned from Lyria API")
            return None

        # Get first prediction
        first_prediction = predictions[0]
        bytes_b64 = first_prediction.get("bytesBase64Encoded")

        if not bytes_b64:
            logger.error("❌ No audio bytes in Lyria response")
            return None

        # Decode audio
        decoded_audio_data = base64.b64decode(bytes_b64)

        # Save to file
        if not output_path:
            os.makedirs("temp_audio", exist_ok=True)
            output_path = os.path.join("temp_audio", "generated_music.wav")

        with open(output_path, "wb") as f:
            f.write(decoded_audio_data)

        logger.info(f"✅ Music generated and saved to: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"❌ Failed to generate music with Lyria: {str(e)}")
        return None
