# SoundTrack Backend

FastAPI-based backend service that handles all API operations, Firebase Firestore database management, and external service integrations.

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/        # Route handlers
│   │   │   ├── media.py     # Media CRUD operations (implemented)
│   │   │   ├── sessions.py  # Session management (placeholder)
│   │   │   └── moods.py     # Mood data (placeholder)
│   │   └── deps/            # Dependencies and middleware
│   ├── core/
│   │   ├── config.py        # Application configuration
│   │   └── database.py      # Database connection
│   ├── models/
│   │   └── media.py         # SQLAlchemy models
│   ├── schemas/
│   │   └── media.py         # Pydantic schemas
│   └── services/            # Business logic (to be implemented)
├── migrations/              # Alembic database migrations
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── alembic.ini             # Database migration config
```

## 🚀 Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Firebase credentials and API keys
   ```

3. **Setup Firebase**:
   ```bash
   # No database setup needed - Firebase is cloud-based!
   # Just ensure your Firebase credentials are properly configured in .env
   ```

4. **Start server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 📊 Firestore Collections

### Implemented Collections

#### `media`
- **Purpose**: Store captured images/clips and their AI analysis
- **Key Fields**: `id`, `session_id`, `ts`, `type`, `storage_url`, `summary`, `elements`
- **API Endpoints**: Full CRUD available at `/api/media`

### Planned Collections
- `sessions` - User sessions
- `mood_events` - EEG/ECG derived mood data
- `songs` - Spotify track metadata
- `song_plays` - Music selection log
- `montages` - Generated video montages

## 🔌 API Endpoints

### Media Management (Implemented)
- `GET /api/media` - List all media items
- `GET /api/media/{id}` - Get specific media item
- `POST /api/media` - Create new media item
- `PUT /api/media/{id}` - Update media item
- `DELETE /api/media/{id}` - Delete media item

### Planned Endpoints
- `/api/sessions` - Session management
- `/api/moods` - Mood events
- `/api/songs` - Spotify integration
- `/api/montages` - Video generation
- `/ws/biometrics` - WebSocket for real-time data

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Configuration

Key environment variables in `.env`:
- `FIREBASE_PROJECT_ID` - Your Firebase project ID
- `FIREBASE_CREDENTIALS_PATH` - Path to service account JSON
- `SPOTIFY_CLIENT_ID/SECRET` - Spotify API credentials
- `GEMINI_API_KEY` - Google AI Studio key
- `OPENAI_API_KEY` - OpenAI API key

## 📖 Development Notes

- Uses Firebase Admin SDK with Firestore
- No database migrations needed (NoSQL document store)
- Pydantic for request/response validation
- CORS enabled for frontend integration
- Async/await support for better performance

## 🚧 To Be Implemented

1. **Biometric Data Processing**: EEG/ECG signal processing pipeline
2. **AI Integrations**: Gemini for image analysis, OpenAI for music recommendations
3. **Spotify Integration**: Track search, playback control, audio features
4. **WebSocket Support**: Real-time biometric data streaming
5. **Video Generation**: Lyria integration and FFmpeg processing
6. **Authentication**: User management and security