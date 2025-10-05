# Firebase Setup Guide for SoundTrack

This guide provides detailed instructions for setting up Firebase for the SoundTrack project.

## 🎯 Overview

SoundTrack uses Firebase for:
- **Firestore**: NoSQL document database for storing media, sessions, and user data
- **Storage**: File storage for images, videos, and audio clips
- **Authentication**: User management (future feature)

## 🔥 Step-by-Step Firebase Setup

### 1. Create Firebase Project

1. **Go to Firebase Console**
   - Visit: https://console.firebase.google.com/
   - Sign in with your Google account

2. **Create New Project**
   - Click "Create a project" or "Add project"
   - Project name: `soundtrack-app` (or your preferred name)
   - Project ID will be auto-generated (note this down!)
   - Enable Google Analytics (recommended but optional)
   - Select analytics location and accept terms

### 2. Enable Firestore Database

1. **Navigate to Firestore**
   - In the Firebase console, click "Firestore Database" in the left sidebar
   - Click "Create database"

2. **Choose Security Rules**
   - **For Development**: Select "Start in test mode"
   - **For Production**: Select "Start in production mode" (requires custom rules)

3. **Select Location**
   - Choose a location closest to your users
   - **Note**: Location cannot be changed after creation!

4. **Firestore is Ready!**
   - You'll see an empty database with no collections yet
   - Collections will be created automatically when the app runs

### 3. Enable Firebase Storage (Optional)

1. **Navigate to Storage**
   - Click "Storage" in the left sidebar
   - Click "Get started"

2. **Security Rules**
   - Start in test mode for development
   - Choose the same location as Firestore

### 4. Get Service Account Credentials

1. **Go to Project Settings**
   - Click the gear icon (⚙️) next to "Project Overview"
   - Select "Project settings"

2. **Navigate to Service Accounts**
   - Click the "Service accounts" tab
   - Select "Firebase Admin SDK"

3. **Generate New Private Key**
   - Click "Generate new private key"
   - A JSON file will be downloaded
   - **Important**: Keep this file secure and never commit to git!

4. **Save the Credentials File**
   ```bash
   # Save in your project root
   mv ~/Downloads/soundtrack-app-*.json ./firebase-service-account.json

   # Add to .gitignore to prevent accidental commits
   echo "firebase-service-account.json" >> .gitignore
   ```

### 5. Configure Environment Variables

1. **Update .env files**
   ```bash
   # In soundtrack/.env
   FIREBASE_PROJECT_ID=your-project-id-from-step-1
   FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json

   # In soundtrack/backend/.env (same values)
   FIREBASE_PROJECT_ID=your-project-id-from-step-1
   FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
   ```

2. **Verify Project ID**
   - Your project ID is visible in the Firebase console URL
   - Format: `https://console.firebase.google.com/project/YOUR-PROJECT-ID`

## 🧪 Test Your Setup

### 1. Test Firebase Connection

```bash
cd backend
python -c "
from app.core.database import initialize_firebase
try:
    db = initialize_firebase()
    print('✅ Firebase connected successfully!')
    print(f'Project ID: {db._client.project}')
except Exception as e:
    print(f'❌ Firebase connection failed: {e}')
"
```

### 2. Test API Endpoints

```bash
# Start the backend server
uvicorn app.main:app --reload --port 8000

# In another terminal, test the media endpoint
curl http://localhost:8000/api/media
# Should return: []

# Create a test media item
curl -X POST http://localhost:8000/api/media \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "type": "image",
    "storage_url": "https://example.com/test.jpg",
    "summary": "Test image from Firebase",
    "elements": ["firebase", "test"]
  }'
```

### 3. Verify in Firebase Console

1. **Check Firestore**
   - Go to Firestore Database in Firebase console
   - You should see a new `media` collection
   - Click on it to see your test document

2. **Document Structure**
   ```json
   {
     "session_id": "test-session-123",
     "type": "image",
     "storage_url": "https://example.com/test.jpg",
     "summary": "Test image from Firebase",
     "elements": ["firebase", "test"],
     "ts": "2024-01-01T12:00:00Z",
     "created_at": "2024-01-01T12:00:00Z",
     "updated_at": "2024-01-01T12:00:00Z"
   }
   ```

## 🔒 Security Considerations

### Development vs Production

**Development Mode (Test Rules)**
```javascript
// Allow read/write access on all documents to any user
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

**Production Mode (Secure Rules)**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can access their own data
    match /media/{mediaId} {
      allow read, write: if request.auth != null;
    }
    match /sessions/{sessionId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Best Practices

1. **Service Account Security**
   - Never commit service account JSON to version control
   - Use environment variables in production
   - Rotate keys regularly

2. **Firestore Rules**
   - Start with test mode for development
   - Implement proper security rules before production
   - Test rules thoroughly

3. **Data Structure**
   - Use meaningful collection and document names
   - Keep document sizes under 1MB
   - Use subcollections for related data

## 🚀 Production Deployment

### Environment Variables

For production deployment, use environment variables instead of files:

```bash
# Set these in your production environment
export FIREBASE_PROJECT_ID="your-project-id"
export FIREBASE_CREDENTIALS_PATH=""  # Leave empty to use default auth

# Or use Firebase credentials JSON as environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### Docker Support

```dockerfile
# In your Dockerfile
COPY firebase-service-account.json /app/
ENV FIREBASE_CREDENTIALS_PATH=/app/firebase-service-account.json
```

## 🔧 Troubleshooting

### Common Issues

1. **"Project not found" Error**
   - Check FIREBASE_PROJECT_ID matches your actual project ID
   - Verify the service account JSON is valid

2. **"Permission denied" Error**
   - Check Firestore security rules
   - Ensure service account has proper permissions

3. **"File not found" Error**
   - Verify FIREBASE_CREDENTIALS_PATH points to the correct file
   - Check file permissions

### Firebase CLI (Optional)

Install Firebase CLI for additional tools:

```bash
# Install
npm install -g firebase-tools

# Login
firebase login

# List projects
firebase projects:list

# Deploy security rules (advanced)
firebase deploy --only firestore:rules
```

## 📝 Next Steps

Once Firebase is working:

1. **Implement Additional Collections**: sessions, mood_events, songs
2. **Add Firebase Storage**: For image and video uploads
3. **Setup Authentication**: User management and security
4. **Optimize Security Rules**: Move from test mode to production rules
5. **Monitor Usage**: Set up Firebase monitoring and alerts

## 🆘 Getting Help

- **Firebase Documentation**: https://firebase.google.com/docs
- **Firestore Documentation**: https://firebase.google.com/docs/firestore
- **Firebase Console**: https://console.firebase.google.com/
- **Stack Overflow**: Tag questions with `firebase` and `firestore`