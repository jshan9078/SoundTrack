# Railway Deployment Guide

This guide explains how to deploy and update the SoundTrack backend on Railway.

## Initial Setup (One-time)

### Prerequisites

- Node.js 18+ (for Railway CLI)
- Git
- Railway account (sign up at https://railway.app)

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login to Railway

```bash
railway login
```

This will open a browser window for authentication.

### 3. Link to Existing Project (if already created)

If the project is already deployed:

```bash
cd backend
railway link
```

Select the existing `htv2025-production` project.

**OR** Create a new project:

```bash
cd backend
railway init
```

### 4. Set Environment Variables

Configure all required environment variables:

```bash
# Firebase Configuration
railway variables set FIREBASE_PROJECT_ID=htv2025-7cc7d
railway variables set STORAGE_BUCKET=htv2025-7cc7d.firebasestorage.app
railway variables set FIREBASE_CREDENTIALS_PATH=htv2025-7cc7d-firebase-adminsdk-fbsvc-b6df0eb1d6.json

# API Keys (replace with your actual keys)
railway variables set GEMINI_API_KEY=your_gemini_api_key
railway variables set SPOTIFY_CLIENT_ID=your_spotify_client_id
railway variables set SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
railway variables set OPENAI_API_KEY=your_openai_api_key
```

### 5. Initial Deployment

```bash
railway up
```

### 6. Get Your Deployment URL

```bash
railway domain
```

Save this URL - you'll need it for the Cloud Function configuration.

### 7. Configure Cloud Function

Set the backend URL for the Cloud Function:

```bash
firebase functions:config:set backend.url="https://your-railway-url.railway.app"
firebase deploy --only functions
```

---

## Updating the Backend (After Code Changes)

Whenever you make changes to the backend code, follow these steps to deploy the updates:

### 1. Navigate to Backend Directory

```bash
cd /Users/jonathan/Desktop/HTV2025/soundtrack/backend
```

### 2. Test Locally First (Recommended)

```bash
# Activate virtual environment
source venv/bin/activate

# Start the backend locally
uvicorn app.main:app --reload --port 8000

# Test your changes at http://localhost:8000/docs
```

### 3. Deploy to Railway

Once you've verified your changes work locally:

```bash
railway up
```

This command will:
- Upload your code to Railway
- Install dependencies from `requirements.txt`
- Restart the server with your changes

### 4. Verify Deployment

Check the deployment logs:

```bash
railway logs
```

Or visit your Railway dashboard: https://railway.app/dashboard

### 5. Test the Live Backend

Visit your deployment URL to verify:
- Health check: `https://your-railway-url.railway.app/health`
- API docs: `https://your-railway-url.railway.app/docs`

---

## Common Railway Commands

### View Logs (Real-time)

```bash
railway logs
```

### View Environment Variables

```bash
railway variables
```

### Add/Update Environment Variable

```bash
railway variables set VARIABLE_NAME=value
```

### Delete Environment Variable

```bash
railway variables delete VARIABLE_NAME
```

### Open Railway Dashboard

```bash
railway open
```

### Check Deployment Status

```bash
railway status
```

---

## Troubleshooting

### Build Fails with Python 3.13 Error

Make sure `runtime.txt` exists in the backend directory with:
```
python-3.12.7
```

### Firebase Credentials Not Found

Ensure the Firebase service account JSON file is in the backend directory and the filename matches `FIREBASE_CREDENTIALS_PATH`.

### Environment Variables Not Loading

- Use `railway variables` to verify all variables are set
- After changing variables, redeploy with `railway up`

### Deployment Successful But Endpoint Returns 500

- Check logs with `railway logs`
- Verify all environment variables are set correctly
- Check that the Firebase credentials file is present

### Port Binding Error

Railway automatically sets the `PORT` environment variable. Make sure your `Procfile` uses `$PORT`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Files Required for Railway Deployment

These files must be in the `backend/` directory:

1. **`requirements.txt`** - Python dependencies
2. **`Procfile`** - Start command for Railway
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. **`runtime.txt`** - Python version
   ```
   python-3.12.7
   ```
4. **Firebase credentials JSON file** - Service account key
5. **`.env`** - Local development only (not deployed to Railway)

---

## Quick Reference

**Deploy changes**: `railway up`

**View logs**: `railway logs`

**Get URL**: `railway domain`

**Open dashboard**: `railway open`
