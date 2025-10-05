# Cloud Functions Setup

## Installation

1. **Install dependencies**:
   ```bash
   cd functions
   npm install
   ```

2. **Login to Firebase**:
   ```bash
   firebase login
   ```

3. **Set your Firebase project**:
   ```bash
   firebase use htv2025-7cc7d
   ```

4. **Configure backend URL**:
   ```bash
   # For production
   firebase functions:config:set backend.url="https://your-backend-url.com"

   # For local testing
   firebase functions:config:set backend.url="http://localhost:8000"
   ```

## Deployment

```bash
# Deploy all functions
firebase deploy --only functions

# Deploy specific function
firebase deploy --only functions:onImageUpload
```

## Testing Locally

1. **Start Firebase emulators**:
   ```bash
   firebase emulators:start
   ```

2. **Upload a test image** to trigger the function

## How It Works

1. Raspberry Pi uploads image → Firebase Storage
2. `onImageUpload` Cloud Function triggers automatically
3. Function calls backend endpoint: `POST /api/media/analyze-new`
4. Backend:
   - Creates Firestore entry
   - Fetches image from storage
   - Analyzes with Gemini (TODO)
   - Updates Firestore with analysis results

## Monitoring

View logs:
```bash
firebase functions:log
```

Real-time logs:
```bash
firebase functions:log --only onImageUpload
```
