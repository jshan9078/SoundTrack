const functions = require('firebase-functions');
const admin = require('firebase-admin');
const axios = require('axios');

admin.initializeApp();

/**
 * Cloud Function that triggers when an image is uploaded to Firebase Storage.
 * Calls the backend analyze endpoint which will:
 * 1. Create the Firestore entry
 * 2. Fetch the image from storage
 * 3. Analyze it with Gemini
 */
exports.onImageUpload = functions.storage.object().onFinalize(async (object) => {
  const filePath = object.name;
  const contentType = object.contentType;
  const bucket = object.bucket;

  // Only process images
  if (!contentType || !contentType.startsWith('image/')) {
    console.log(`Skipping non-image file: ${filePath}`);
    return null;
  }

  console.log(`New image uploaded: ${filePath}`);

  const storageUrl = `https://storage.googleapis.com/${bucket}/${filePath}`;

  // Get backend URL from environment config
  // Set this with: firebase functions:config:set backend.url="http://your-backend-url:8000"
  const backendUrl = functions.config().backend?.url || 'http://localhost:8000';

  try {
    // Call backend analyze endpoint with storage URL
    const response = await axios.post(`${backendUrl}/api/media/analyze-new`, {
      storage_url: storageUrl,
      type: 'image'
    }, {
      timeout: 60000 // 60 second timeout for Gemini processing
    });

    console.log(`Analysis triggered successfully for: ${filePath}`);
    console.log(`Response:`, response.data);

    return null;
  } catch (error) {
    console.error(`Failed to trigger analysis for ${filePath}:`, error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
    // Don't throw - we don't want to retry on permanent failures
    return null;
  }
});

/**
 * Cloud Function that triggers when a new document is created in the media collection.
 * Checks if the document has processed_at field (meaning Gemini analysis is complete),
 * then calls the backend recommend-song endpoint.
 */
exports.onMediaCreated = functions.firestore
  .document('media/{mediaId}')
  .onCreate(async (snapshot, context) => {
    const mediaId = context.params.mediaId;
    const data = snapshot.data();

    // Check if analysis is complete (has processed_at field)
    if (data.processed_at) {
      console.log(`New media created with analysis: ${mediaId}`);
      console.log(`Mood: ${data.mood}`);
      console.log(`Summary: ${data.summary}`);

      const backendUrl = functions.config().backend?.url || 'http://localhost:8000';

      try {
        // Call backend recommend-song endpoint
        const response = await axios.post(`${backendUrl}/api/media/recommend-song`, null, {
          params: { media_id: mediaId },
          timeout: 30000 // 30 second timeout
        });

        console.log(`Song recommendation triggered for: ${mediaId}`);
        console.log(`Response:`, response.data);

        return null;
      } catch (error) {
        console.error(`Failed to trigger song recommendation for ${mediaId}:`, error.message);
        if (error.response) {
          console.error('Response data:', error.response.data);
          console.error('Response status:', error.response.status);
        }
        // Don't throw - we don't want to retry on permanent failures
        return null;
      }
    } else {
      console.log(`Media created but analysis not complete yet: ${mediaId}`);
      return null;
    }
  });
