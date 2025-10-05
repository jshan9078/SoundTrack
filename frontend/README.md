# SoundTrack Frontend

Next.js-based frontend application with a Spotify-inspired design for visualizing your daily soundtrack and biometric data.

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css      # Global styles with Tailwind
│   │   ├── layout.tsx       # Root layout component
│   │   └── page.tsx         # Main dashboard page (implemented)
│   ├── components/          # Reusable React components (to be added)
│   ├── hooks/              # Custom React hooks (to be added)
│   ├── types/
│   │   └── index.ts        # TypeScript type definitions
│   └── utils/              # Utility functions (to be added)
├── public/                 # Static assets
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
└── next.config.js         # Next.js configuration
```

## 🎨 Design System

### Color Palette
- **Primary**: Spotify Green (`#1DB954`)
- **Background**: Dark theme (`#121212`, `#191414`)
- **Cards**: Dark gray (`#282828`)
- **Text**: White with gray variants

### Key Components (Implemented)
- **Dashboard Layout**: Main page with header, timeline, and playlist sidebar
- **Timeline View**: Shows media captures with AI analysis
- **Playlist Sidebar**: Displays daily tracks with mood indicators
- **Responsive Design**: Works on desktop and mobile

## 🚀 Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with API URL
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Access application**:
   - Development: http://localhost:3000
   - Production build: `npm run build && npm start`

## 📦 Dependencies

### Core
- **Next.js 14**: React framework with App Router
- **React 18**: UI library
- **TypeScript**: Type safety

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library

### Data & Charts
- **Recharts**: Chart library for biometric data visualization
- **Axios**: HTTP client for API calls

## 🧩 Components Structure

### Current Implementation
```tsx
// Main Dashboard (app/page.tsx)
├── Header (Navigation)
├── Main Content (Timeline)
│   ├── EEG/ECG Chart Placeholder
│   └── Media Timeline Items
└── Sidebar (Daily Playlist)
    ├── Track Cards
    └── Video Generation Button
```

### Planned Components
- `<BiometricChart />` - Real-time EEG/ECG visualization
- `<MediaCard />` - Individual media item display
- `<TrackCard />` - Spotify track with mood indicator
- `<VideoPlayer />` - Montage video player
- `<MoodIndicator />` - Visual mood representation

## 🔧 Configuration

### Next.js Config
- **API Proxy**: Forwards `/api/*` to backend at `localhost:8000`
- **App Directory**: Uses new App Router architecture

### Tailwind Config
- **Custom Colors**: Spotify theme colors
- **Component Path**: Includes all src files

## 📱 Features

### Implemented
- **Responsive Dashboard**: Main interface with dummy data
- **Timeline View**: Shows captured media with AI summaries
- **Playlist Sidebar**: Daily tracks with mood indicators
- **Loading States**: Spinner animations for data fetching

### To Be Implemented
1. **Real-time Data**: WebSocket connection for live biometric data
2. **Interactive Charts**: Recharts integration for EEG/ECG visualization
3. **Media Gallery**: Full-screen media viewer
4. **Video Playground**: Hour selection and montage generation
5. **Settings Panel**: User preferences and calibration
6. **Audio Controls**: Spotify playback integration

## 🔌 API Integration

### Current
- Basic structure for media API calls
- Type definitions for all data models

### Planned
- Real-time WebSocket connection
- Spotify Web Playback SDK
- File upload for media
- Video streaming for montages

## 🎯 Development Guidelines

### Styling
- Use Tailwind utility classes
- Follow Spotify design patterns
- Maintain dark theme consistency
- Use responsive breakpoints

### State Management
- React hooks for local state
- Consider Zustand for global state
- Real-time updates via WebSocket

### Performance
- Image optimization with Next.js
- Lazy loading for media content
- Chart data virtualization
- Code splitting for routes

## 🧪 Testing

```bash
# Lint code
npm run lint

# Type checking
npx tsc --noEmit

# Future: Add Jest/Testing Library
npm test
```

## 🚧 Roadmap

1. **Phase 1**: Complete dashboard with real API integration
2. **Phase 2**: Add biometric data visualization
3. **Phase 3**: Implement video playground
4. **Phase 4**: Add voice controls and advanced features
5. **Phase 5**: Mobile app with React Native