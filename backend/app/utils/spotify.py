import requests
import base64
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_spotify_token() -> Optional[str]:
    """
    Get Spotify access token using client credentials flow.
    Returns the bearer token or None if failed.
    """
    if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
        logger.error("Spotify credentials not configured")
        return None

    # Encode client credentials
    auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    # Request access token
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        logger.error(f"Failed to get Spotify token: {str(e)}")
        return None

def search_track(song_name: str, artist_name: str) -> Optional[Dict[str, Any]]:
    """
    Search for a track on Spotify.
    Returns track data including name, artist, and embed link.
    """
    token = get_spotify_token()
    if not token:
        return None

    # Build search query
    query = f"track:{song_name} artist:{artist_name}"

    # Search for track
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        tracks = data.get("tracks", {}).get("items", [])
        if not tracks:
            logger.warning(f"No Spotify track found for: {song_name} by {artist_name}")
            return None

        track = tracks[0]

        # Extract track info
        track_id = track.get("id")
        track_name = track.get("name")
        track_artists = ", ".join([artist.get("name") for artist in track.get("artists", [])])
        embed_url = f"https://open.spotify.com/embed/track/{track_id}"

        logger.info(f"✅ Found Spotify track: {track_name} by {track_artists}")

        return {
            "song": track_name,
            "song_artist": track_artists,
            "embed": embed_url,
            "spotify_id": track_id
        }

    except Exception as e:
        logger.error(f"Failed to search Spotify track: {str(e)}")
        return None
