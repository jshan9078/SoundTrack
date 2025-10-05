'use client'

import { useState, useEffect } from 'react'
import { Play, Heart, BarChart3, Camera } from 'lucide-react'

interface MediaItem {
  id: string
  type: string
  summary?: string
  elements?: string[]
  ts: string
}

export default function Dashboard() {
  const [mediaItems, setMediaItems] = useState<MediaItem[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setMediaItems([
        {
          id: '1',
          type: 'image',
          summary: 'User working at desk with laptop and coffee',
          elements: ['laptop', 'coffee', 'desk', 'books'],
          ts: new Date().toISOString()
        },
        {
          id: '2',
          type: 'image',
          summary: 'Beautiful sunset view from window',
          elements: ['sunset', 'window', 'trees', 'sky'],
          ts: new Date(Date.now() - 3600000).toISOString()
        }
      ])
      setIsLoading(false)
    }, 1000)
  }, [])

  return (
    <div className="min-h-screen bg-spotify-gray text-white">
      {/* Header */}
      <header className="bg-spotify-black p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-spotify-green">SoundTrack</h1>
          <nav className="flex gap-6">
            <button className="hover:text-spotify-green transition-colors">Dashboard</button>
            <button className="hover:text-spotify-green transition-colors">Playlist</button>
            <button className="hover:text-spotify-green transition-colors">Analytics</button>
          </nav>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Timeline */}
          <div className="lg:col-span-3">
            <div className="bg-spotify-lightgray rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Today's Timeline
              </h2>

              {/* Sample EEG Chart Placeholder */}
              <div className="mb-6 h-32 bg-gray-800 rounded-lg flex items-center justify-center">
                <p className="text-gray-400">EEG/ECG Chart Placeholder</p>
              </div>

              {/* Media Timeline */}
              <div className="space-y-4">
                {isLoading ? (
                  <div className="flex justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-spotify-green"></div>
                  </div>
                ) : (
                  mediaItems.map((item) => (
                    <div key={item.id} className="bg-gray-800 rounded-lg p-4 flex items-center gap-4">
                      <div className="w-16 h-16 bg-gray-700 rounded-lg flex items-center justify-center">
                        <Camera className="w-6 h-6 text-gray-400" />
                      </div>
                      <div className="flex-1">
                        <p className="font-medium">{item.summary}</p>
                        <div className="flex gap-2 mt-1">
                          {item.elements?.map((element, idx) => (
                            <span key={idx} className="px-2 py-1 bg-spotify-green/20 text-spotify-green text-xs rounded">
                              {element}
                            </span>
                          ))}
                        </div>
                        <p className="text-sm text-gray-400 mt-1">
                          {new Date(item.ts).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Sidebar - Daily Playlist */}
          <div className="bg-spotify-lightgray rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Today's Playlist</h3>

            {/* Sample playlist items */}
            <div className="space-y-3">
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-spotify-green rounded-lg flex items-center justify-center">
                    <Play className="w-4 h-4 text-black" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-sm truncate">Lofi Study Beats</p>
                    <p className="text-xs text-gray-400 truncate">ChilledCow</p>
                  </div>
                  <button className="text-gray-400 hover:text-red-500">
                    <Heart className="w-4 h-4" />
                  </button>
                </div>
                <div className="mt-2">
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded">Focused</span>
                </div>
              </div>

              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                    <Play className="w-4 h-4 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-sm truncate">Golden Hour</p>
                    <p className="text-xs text-gray-400 truncate">Kacey Musgraves</p>
                  </div>
                  <button className="text-gray-400 hover:text-red-500">
                    <Heart className="w-4 h-4" />
                  </button>
                </div>
                <div className="mt-2">
                  <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded">Happy</span>
                </div>
              </div>
            </div>

            {/* Video Playground Button */}
            <button className="w-full mt-6 bg-spotify-green text-black font-semibold py-2 rounded-lg hover:bg-spotify-green/90 transition-colors">
              Create Daily Video
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}