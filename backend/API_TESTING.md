# API Testing Guide

This guide shows how to test the SoundTrack backend API endpoints without a frontend, using `curl` commands from your terminal.

## Prerequisites

1. **Start the backend server**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

2. **Verify the server is running**:
   ```bash
   curl http://localhost:8000/health
   ```
   Expected response: `{"status":"healthy","database":"firebase"}`

---

## Media Endpoints

### 1. Create a Media Item

Upload media metadata (note: this stores metadata, not the actual file upload):

```bash
curl -X POST http://localhost:8000/api/media/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "storage_url": "https://storage.googleapis.com/htv2025-7cc7d.firebasestorage.app/test-image.jpg",
    "thumb_url": "https://storage.googleapis.com/htv2025-7cc7d.firebasestorage.app/test-image-thumb.jpg",
    "summary": "A beautiful sunset photo",
    "tags": ["sunset", "nature", "photography"]
  }'
```

**Response**: Returns the created media item with an auto-generated `id`.

### 2. Get All Media Items

```bash
curl http://localhost:8000/api/media/
```

**With pagination**:
```bash
curl "http://localhost:8000/api/media/?skip=0&limit=10"
```

### 3. Get a Specific Media Item

Replace `{media_id}` with the actual ID from the create response:

```bash
curl http://localhost:8000/api/media/{media_id}
```

### 4. Update a Media Item

```bash
curl -X PUT http://localhost:8000/api/media/{media_id} \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Updated: A stunning sunset over the mountains",
    "tags": ["sunset", "nature", "mountains", "golden-hour"]
  }'
```

### 5. Delete a Media Item

```bash
curl -X DELETE http://localhost:8000/api/media/{media_id}
```

---

## File Upload to Firebase Storage (Manual Testing)

To test actual file uploads to Firebase Storage, you can use Python:

### Upload Script

Use the existing `test_upload.py` file in the backend directory. Just update the image path before running:

```bash
python test_upload.py
```

### Complete Workflow Test

1. **Upload an image to Firebase Storage** (using the script above)
2. **Create media metadata** referencing the uploaded file:
   ```bash
   curl -X POST http://localhost:8000/api/media/ \
     -H "Content-Type: application/json" \
     -d '{
       "type": "image",
       "storage_url": "https://storage.googleapis.com/htv2025-7cc7d.firebasestorage.app/test-uploads/image.jpg",
       "summary": "Test upload"
     }'
   ```
3. **Fetch the metadata from Firestore**:
   ```bash
   curl http://localhost:8000/api/media/
   ```

---

## Moods Endpoints (Placeholder)

```bash
# Get moods
curl http://localhost:8000/api/moods/

# Create mood
curl -X POST http://localhost:8000/api/moods/
```

---

## Using HTTPie (Alternative to curl)

Install HTTPie for a more user-friendly experience:
```bash
pip install httpie
```

### Examples with HTTPie:

```bash
# Create media
http POST localhost:8000/api/media/ \
  type=image \
  storage_url=https://example.com/image.jpg \
  summary="Test image"

# Get all media
http GET localhost:8000/api/media/

# Update media
http PUT localhost:8000/api/media/{media_id} \
  summary="Updated summary"
```

---

## Using Postman

1. Import the base URL: `http://localhost:8000`
2. Create requests for each endpoint
3. Use the JSON payloads from the examples above

---

## Troubleshooting

- **404 errors**: Check that the server is running on port 8000
- **Firebase errors**: Verify `.env` file has correct `FIREBASE_PROJECT_ID` and `FIREBASE_CREDENTIALS_PATH`
- **CORS errors**: Not applicable for curl/terminal testing, only affects browser requests
