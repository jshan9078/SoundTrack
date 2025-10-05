export interface MediaItem {
  id: string
  session_id: string
  ts: string
  type: 'image' | 'clip'
  storage_url: string
  thumb_url?: string
  duration_sec?: number
  summary?: string
  elements?: string[]
  tags?: string[]
}

export interface MoodEvent {
  ts: string
  label: 'Calm' | 'Focused' | 'Energetic' | 'Melancholic' | 'Happy' | 'Anxious' | 'Neutral'
  confidence: number
  features: {
    eeg: Record<'delta' | 'theta' | 'alpha' | 'beta' | 'gamma', number>
    eegRatios: Record<string, number>
    ecg: { hr: number; rmssd?: number; sdnn?: number; lfHf?: number }
    imu?: { activity: number }
  }
}

export interface SpotifyTrack {
  id: string
  title: string
  artist: string
  album: string
  albumArtUrl: string
  durationMs: number
  audioFeatures?: {
    bpm?: number
    key?: number
    mode?: 0 | 1
    energy?: number
    valence?: number
    danceability?: number
    acousticness?: number
    instrumentalness?: number
  }
}

export interface TimelineItem {
  kind: 'media' | 'song'
  ts: string
  mediaId?: string
  thumbUrl?: string
  summary?: string
  elements?: string[]
  track?: SpotifyTrack
  mood?: MoodEvent['label']
}