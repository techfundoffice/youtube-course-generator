import { useEffect, useRef, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Play, 
  Download, 
  ExternalLink, 
  Cloud, 
  AlertTriangle,
  Youtube,
  Video
} from 'lucide-react'

interface VideoInfo {
  title: string
  author: string
  duration?: string
  view_count?: number
  published_at?: string
  thumbnail_url?: string
  mp4_video_url?: string
  mp4_file_size?: number
  mp4_download_status?: string
  cloudinary_url?: string
  cloudinary_thumbnail?: string
  source?: string
}

interface AdvancedVideoPlayerProps {
  videoInfo: VideoInfo
  youtubeUrl?: string
  videoId?: string
  courseId?: string | number
  className?: string
}

export default function AdvancedVideoPlayer({ 
  videoInfo, 
  youtubeUrl, 
  videoId, 
  courseId,
  className = '' 
}: AdvancedVideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [videoError, setVideoError] = useState(false)
  const [showYoutube, setShowYoutube] = useState(false)

  useEffect(() => {
    // Initialize video.js-like functionality
    const video = videoRef.current
    if (video) {
      video.addEventListener('error', () => setVideoError(true))
      
      return () => {
        video.removeEventListener('error', () => setVideoError(true))
      }
    }
  }, [])

  const videoSource = videoInfo.cloudinary_url || videoInfo.mp4_video_url
  const poster = videoInfo.cloudinary_thumbnail || videoInfo.thumbnail_url

  return (
    <div className={`space-y-6 ${className}`}>
      {/* YouTube Video Embed */}
      {videoId && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Youtube className="h-5 w-5 text-red-500" />
              <span>YouTube Video</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="aspect-video rounded-lg overflow-hidden">
              <iframe 
                src={`https://www.youtube.com/embed/${videoId}`}
                frameBorder="0" 
                allowFullScreen
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                className="w-full h-full"
              />
            </div>
            <div className="mt-3">
              <Button variant="outline" size="sm" asChild>
                <a href={youtubeUrl} target="_blank" rel="noopener noreferrer">
                  <Youtube className="h-4 w-4 mr-2" />
                  View on YouTube
                </a>
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* MP4 Video Player */}
      {videoSource ? (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Video className="h-5 w-5" />
              <span>Original Video</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* Premium Storage Indicator */}
            {videoInfo.cloudinary_url && (
              <Alert className="mb-4">
                <Cloud className="h-4 w-4" />
                <AlertDescription>
                  <strong>Premium Storage:</strong> This video is stored in Cloudinary premium cloud storage for persistent access.
                </AlertDescription>
              </Alert>
            )}
            
            <div className="aspect-video rounded-lg overflow-hidden bg-black">
              {!videoError ? (
                <video
                  ref={videoRef}
                  controls
                  preload="auto"
                  className="w-full h-full"
                  poster={poster}
                  onError={() => setVideoError(true)}
                >
                  <source src={videoSource} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-900 text-white">
                  <div className="text-center">
                    <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-yellow-500" />
                    <p className="mb-4">Video playback failed</p>
                    <Button variant="outline" asChild>
                      <a href={videoSource} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4 mr-2" />
                        Try Direct Link
                      </a>
                    </Button>
                  </div>
                </div>
              )}
            </div>
            
            <div className="mt-3">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                <div className="text-sm text-muted-foreground">
                  <Download className="inline h-4 w-4 mr-1" />
                  Download Status: 
                  <Badge 
                    variant={videoInfo.mp4_download_status === 'completed' ? 'default' : 'outline'}
                    className={videoInfo.mp4_download_status === 'completed' ? 'bg-green-500 ml-2' : 'ml-2'}
                  >
                    {videoInfo.mp4_download_status?.replace('_', ' ').toUpperCase() || 'AVAILABLE'}
                  </Badge>
                  {videoInfo.source === 'youtube-downloader' && (
                    <div className="text-yellow-500 text-xs mt-1">
                      <AlertTriangle className="inline h-3 w-3 mr-1" />
                      Free fallback system used
                    </div>
                  )}
                </div>
                
                {videoInfo.mp4_file_size && (
                  <div className="text-sm text-muted-foreground">
                    <Video className="inline h-4 w-4 mr-1" />
                    File Size: {(videoInfo.mp4_file_size / 1024 / 1024).toFixed(1)} MB
                  </div>
                )}
              </div>
              
              <div className="flex flex-wrap gap-2">
                <Button variant="outline" size="sm" asChild>
                  <a href={videoSource} target="_blank" download>
                    <Download className="h-4 w-4 mr-2" />
                    Download Video
                  </a>
                </Button>
                
                {youtubeUrl && (
                  <Button variant="outline" size="sm" asChild>
                    <a href={youtubeUrl} target="_blank" rel="noopener noreferrer">
                      <Youtube className="h-4 w-4 mr-2" />
                      View on YouTube
                    </a>
                  </Button>
                )}
                
                {courseId && (
                  <Button variant="outline" size="sm" asChild>
                    <a href={`/download/${courseId}`}>
                      <Download className="h-4 w-4 mr-2" />
                      Download Course Package
                    </a>
                  </Button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        /* Debug Info: No MP4 Video Available */
        <Card>
          <CardContent className="py-6">
            <Alert>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <strong>MP4 Video Not Available</strong>
                <p className="mt-2">The MP4 video download may have failed or is still in progress. The course content is available below.</p>
                <div className="mt-3">
                  {youtubeUrl && (
                    <Button variant="outline" size="sm" asChild>
                      <a href={youtubeUrl} target="_blank" rel="noopener noreferrer">
                        <Youtube className="h-4 w-4 mr-2" />
                        View on YouTube
                      </a>
                    </Button>
                  )}
                </div>
                <div className="text-xs text-muted-foreground mt-2 font-mono">
                  Debug info: mp4_video_url = "{videoInfo.mp4_video_url || 'Not set'}", 
                  mp4_download_status = "{videoInfo.mp4_download_status || 'Not set'}"
                </div>
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}
    </div>
  )
}