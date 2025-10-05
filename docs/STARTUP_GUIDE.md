# SoundTrack - Complete Startup Guide

This guide will walk you through setting up the entire SoundTrack development environment from scratch.

## 📋 Prerequisites

Before starting, ensure you have the following installed:

### Required Software
- **Python 3.8+**: [Download from python.org](https://www.python.org/downloads/)
- **Node.js 18+**: [Download from nodejs.org](https://nodejs.org/)
- **PostgreSQL 12+**: [Download from postgresql.org](https://www.postgresql.org/download/)
- **Git**: [Download from git-scm.com](https://git-scm.com/)

### Optional (Recommended)
- **Docker**: For easy PostgreSQL setup
- **VS Code**: With Python and TypeScript extensions

## 🔑 API Keys Setup

You'll need to obtain API keys from these services:

### 1. Spotify Developer Account
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in app details:
   - App name: "SoundTrack"
   - Description: "AI-powered soundtrack for your life"
   - Redirect URI: `http://localhost:3000/callback`
5. Save the **Client ID** and **Client Secret**

### 2. Google AI Studio (Gemini)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new project or select existing
4. Go to "API Keys" section
5. Click "Create API Key"
6. Save the **API Key**

### 3. OpenAI API
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create new secret key"
5. Save the **API Key**

## 🗄️ Firebase Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: "soundtrack-app" (or your preferred name)
4. Enable Google Analytics (optional)
5. Choose your analytics location and accept terms

### 2. Enable Firestore Database
1. In your Firebase project, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location for your database (choose closest to your users)

### 3. Get Service Account Credentials
1. Go to Project Settings (gear icon) → "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Save it in your project directory as `firebase-service-account.json`
5. Keep this file secure and never commit it to version control!

## 🚀 Project Setup

### 1. Clone Repository (or navigate to your project)
```bash
cd soundtrack
```

### 2. Environment Configuration
```bash
# Copy global environment template
cp .env.example .env

# Edit the global .env file with your API keys
nano .env  # or use your preferred editor
```

Fill in your API keys:
```env
# API Keys
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Firebase
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
```

## 🔧 Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Backend Environment
```bash
cp .env.example .env
# Edit backend/.env with the same values as the global .env
```

### 5. Verify Firebase Setup
```bash
# Test Firebase connection
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

### 6. Start Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

**✅ Backend should now be running at http://localhost:8000**

### 7. Test Backend
Open another terminal and test:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# Test API docs
open http://localhost:8000/docs  # Opens Swagger UI
```

## 🎨 Frontend Setup

### 1. Navigate to Frontend Directory
```bash
# From project root
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Frontend Environment
```bash
cp .env.example .env
# Edit frontend/.env
```

Content should be:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Start Frontend Server
```bash
npm run dev
```

**✅ Frontend should now be running at http://localhost:3000**

## 🧪 Testing the Setup

### 1. Test Frontend-Backend Communication
1. Open http://localhost:3000
2. You should see the SoundTrack dashboard
3. Open browser developer tools (F12)
4. Check for any errors in the console

### 2. Test Firebase Connection
```bash
# In backend directory
python -c "
from app.models.media import MediaModel
try:
    media_model = MediaModel()
    print('✅ Firestore connection successful!')
    print('Collections accessible')
except Exception as e:
    print(f'❌ Firestore connection failed: {e}')
"
```

### 3. Test API Endpoints
```bash
# Test media endpoint
curl -X GET http://localhost:8000/api/media
# Should return empty array: []

# Create a test media item
curl -X POST http://localhost:8000/api/media \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "type": "image",
    "storage_url": "https://example.com/test.jpg",
    "summary": "Test image",
    "elements": ["test", "example"]
  }'
```

## 🔧 Troubleshooting

### Common Issues

#### "ModuleNotFoundError" in Backend
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Firebase Connection Error
```bash
# Check Firebase credentials
echo $FIREBASE_PROJECT_ID
ls -la firebase-service-account.json

# Verify service account has proper permissions
# The JSON file should contain:
# - "type": "service_account"
# - "project_id": "your-project-id"
# - "private_key_id" and "private_key"

# Test Firebase CLI (optional)
npm install -g firebase-tools
firebase login
firebase projects:list
```

#### Frontend Build Errors
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
uvicorn app.main:app --reload --port 8001
```

### Environment Variable Issues
1. Ensure `.env` files are in correct directories
2. Check for typos in variable names
3. Restart servers after changing environment variables
4. Use `python -c "from app.core.config import settings; print(settings.FIREBASE_PROJECT_ID)"` to verify backend config

## 📝 Development Workflow

### Daily Development Routine
1. **Firebase**: Always available (cloud-based) ✨
2. **Start Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```
3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Making Database Changes
1. Edit models in `backend/app/models/`
2. No migrations needed! Firestore is schemaless
3. Collections and documents are created automatically

### Adding New API Endpoints
1. Create endpoint in `backend/app/api/endpoints/`
2. Add router to `backend/app/main.py`
3. Test with Swagger UI at http://localhost:8000/docs

## 🎯 Next Steps

Once everything is running:
1. Check out the [Implementation Checklist](IMPLEMENTATION_CHECKLIST.md)
2. Review the project structure in individual README files
3. Start implementing features according to the roadmap

## 📞 Support

If you encounter issues:
1. Check the individual README files in backend/ and frontend/
2. Review error logs in terminal output
3. Test API endpoints using the Swagger UI at http://localhost:8000/docs