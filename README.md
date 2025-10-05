# SoundTrack - A Soundtrack to Your Life

SoundTrack is an AI-powered application that creates a personalized soundtrack based on your mood, environment, and biomedical data. It captures your daily experiences through images, analyzes your emotional state through EEG/ECG data, and automatically selects music that matches your current state.

## 🎯 Key Features

- **Real-time Mood Detection**: Uses EEG and ECG data to determine emotional state
- **Environment Analysis**: AI-powered image analysis to understand surroundings
- **Smart Music Selection**: Intelligent song recommendations via Spotify API
- **Daily Video Montages**: Auto-generated videos with custom soundtracks
- **Beautiful Dashboard**: Spotify-like interface with timeline and analytics

## 🏗️ Project Structure

```
soundtrack/
├── backend/           # FastAPI backend application
├── frontend/          # Next.js frontend application
├── docs/             # Documentation and guides
├── scripts/          # Utility scripts
├── .env.example      # Environment variables template
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Firebase Setup

1. **Create Firebase Project**:
   - Go to https://console.firebase.google.com/
   - Create a new project (or select existing)
   - Enable Firestore Database
   - Enable Firebase Storage

2. **Download Service Account Credentials**:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file to `HTV2025/` (parent directory)

3. **Note your Storage Bucket**:
   - Go to Storage in Firebase Console
   - Copy your bucket URL (e.g., `project-id.firebasestorage.app`)

### 2. Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create Python virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # On macOS/Linux in EACH NEW TERMINAL:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Edit `backend/.env` and update:
     ```
     FIREBASE_PROJECT_ID=your-project-id
     FIREBASE_CREDENTIALS_PATH=path-to-service-account.json
     STORAGE_BUCKET=your-project.firebasestorage.app
     SPOTIFY_CLIENT_ID=your_spotify_client_id
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
     GEMINI_API_KEY=your_gemini_api_key
     ```

6. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

7. **Verify backend is running**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### 3. Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   - Edit `frontend/.env.local`:
     ```
     NEXT_PUBLIC_API_URL=http://localhost:8000
     PORT=3000
     ```

4. **Start the frontend server**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000

### 4. Cloud Functions Setup (Optional - for Raspberry Pi auto-trigger)

1. **Install Firebase CLI**:
   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase**:
   ```bash
   firebase login
   ```

3. **Install function dependencies**:
   ```bash
   cd functions
   npm install
   ```

4. **Configure backend URL**:
   ```bash
   firebase functions:config:set backend.url="http://your-backend-url:8000"
   ```

5. **Deploy Cloud Functions**:
   ```bash
   firebase deploy --only functions
   ```

### 5. Testing Image Upload

1. **Make sure backend is running** (see Backend Setup step 6)

2. **Update test image path** in `backend/test_upload.py`:
   ```python
   local_image = "path/to/your/image.jpg"
   ```

3. **Run the upload script**:
   ```bash
   cd backend
   source venv/bin/activate  # Make sure venv is activated
   python test_upload.py
   ```

4. **Verify**:
   - Check Firebase Storage for uploaded image
   - Check Firestore for created media entry
   - Check backend logs for processing confirmation

## 📋 Prerequisites

- **Python 3.8-3.12** (NOT 3.13 - see troubleshooting below)
- Node.js 18+
- Firebase Project
- Spotify Developer Account
- Google AI Studio Account (for Gemini)
- OpenAI API Key

## 🔑 Required Setup

1. **Firebase**: Create project at https://console.firebase.google.com/
2. **Spotify**: Create app at https://developer.spotify.com/
3. **Gemini**: Get key from https://aistudio.google.com/
4. **OpenAI**: Get key from https://platform.openai.com/

## 📖 Documentation

- [Backend README](./backend/README.md) - API documentation and backend setup
- [Frontend README](./frontend/README.md) - Frontend architecture and components
- [Startup Guide](./docs/STARTUP_GUIDE.md) - Detailed setup instructions
- [Implementation Checklist](./docs/IMPLEMENTATION_CHECKLIST.md) - Development roadmap

## 🛠️ Development

This is a hackathon starter repository with basic CRUD operations. See the implementation checklist for the full feature roadmap.

## 🐛 Troubleshooting

### Python 3.13 Compatibility Issue

**Error**: `Failed building wheel for pydantic-core` when running `pip install -r requirements.txt`

**Cause**: Python 3.13 has breaking changes that are incompatible with the current version of pydantic-core.

**Solution**: Use Python 3.12 or earlier

1. **Check if you have Python 3.12**:
   ```bash
   python3.12 --version
   ```

2. **If not installed, install Python 3.12**:
   ```bash
   # On macOS:
   brew install python@3.12

   # On Ubuntu/Debian:
   sudo apt install python3.12 python3.12-venv

   # On Windows:
   # Download from https://www.python.org/downloads/
   ```

3. **Recreate virtual environment with Python 3.12**:
   ```bash
   cd backend
   rm -rf venv
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Backend Logs Not Showing

If you don't see detailed logs when the Cloud Function calls the backend, make sure you're running uvicorn with the `--reload` flag:

```bash
uvicorn app.main:app --reload --port 8000
```

### Cloud Function Not Triggering

1. Check Cloud Function logs:
   ```bash
   firebase functions:log
   ```

2. Verify the backend URL is configured:
   ```bash
   firebase functions:config:get
   ```

3. Ensure Firebase Storage bucket matches in:
   - Cloud Function deployment
   - Backend `.env` file
   - Raspberry Pi upload script

## 📝 License

MIT License - see LICENSE file for details