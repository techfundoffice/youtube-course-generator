import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Link, 
  Youtube, 
  Download, 
  Check, 
  AlertTriangle,
  Shield,
  ExternalLink
} from 'lucide-react'

interface VideoInfo {
  mp4_video_url?: string
  mp4_download_status?: string
  mp4_file_size?: number
  source?: string
}

interface URLComparisonTableProps {
  youtubeUrl: string
  videoInfo: VideoInfo
  className?: string
}

export default function URLComparisonTable({ 
  youtubeUrl, 
  videoInfo, 
  className = '' 
}: URLComparisonTableProps) {
  const getStatusBadge = (status?: string, source?: string) => {
    if (status === 'completed_fallback' || source === 'youtube-downloader') {
      return (
        <Badge variant="default" className="bg-yellow-500">
          <Shield className="h-3 w-3 mr-1" />
          Completed (Fallback System)
        </Badge>
      )
    }
    
    if (status === 'completed') {
      return (
        <Badge variant="default" className="bg-green-500">
          <Check className="h-3 w-3 mr-1" />
          Completed
        </Badge>
      )
    }
    
    return (
      <Badge variant="outline">
        <AlertTriangle className="h-3 w-3 mr-1" />
        {status?.replace('_', ' ').toUpperCase() || 'Available'}
      </Badge>
    )
  }

  if (!youtubeUrl || !videoInfo.mp4_video_url) {
    return null
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Link className="h-5 w-5" />
          <span>URL Comparison Table</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3 font-medium">Source Type</th>
                <th className="text-left p-3 font-medium">URL</th>
                <th className="text-left p-3 font-medium">Status</th>
                <th className="text-left p-3 font-medium">File Size</th>
                <th className="text-left p-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {/* YouTube Row */}
              <tr className="border-b">
                <td className="p-3">
                  <div className="flex items-center space-x-2">
                    <Youtube className="h-4 w-4 text-red-500" />
                    <strong>Original YouTube</strong>
                  </div>
                </td>
                <td className="p-3">
                  <code className="text-xs bg-muted px-2 py-1 rounded break-all">
                    {youtubeUrl}
                  </code>
                </td>
                <td className="p-3">
                  <Badge variant="default" className="bg-green-500">
                    <Check className="h-3 w-3 mr-1" />
                    Active
                  </Badge>
                </td>
                <td className="p-3">
                  <span className="text-muted-foreground">Streaming</span>
                </td>
                <td className="p-3">
                  <Button variant="outline" size="sm" asChild>
                    <a href={youtubeUrl} target="_blank" rel="noopener noreferrer">
                      <Youtube className="h-3 w-3 mr-1" />
                      Watch
                    </a>
                  </Button>
                </td>
              </tr>

              {/* MP4 Download Row */}
              <tr className="border-b">
                <td className="p-3">
                  <div className="flex items-center space-x-2">
                    <Download className="h-4 w-4 text-blue-500" />
                    <strong>Downloaded MP4</strong>
                  </div>
                </td>
                <td className="p-3">
                  <code className="text-xs bg-muted px-2 py-1 rounded break-all">
                    {videoInfo.mp4_video_url}
                  </code>
                </td>
                <td className="p-3">
                  <div className="space-y-1">
                    {getStatusBadge(videoInfo.mp4_download_status, videoInfo.source)}
                    {videoInfo.source === 'youtube-downloader' && (
                      <div className="text-xs text-yellow-600">
                        <AlertTriangle className="inline h-3 w-3 mr-1" />
                        Free fallback system used
                      </div>
                    )}
                  </div>
                </td>
                <td className="p-3">
                  {videoInfo.mp4_file_size ? (
                    <span className="text-blue-600 font-medium">
                      {(videoInfo.mp4_file_size / 1024 / 1024).toFixed(1)} MB
                    </span>
                  ) : (
                    <span className="text-muted-foreground">Unknown</span>
                  )}
                </td>
                <td className="p-3">
                  <Button variant="outline" size="sm" asChild>
                    <a href={videoInfo.mp4_video_url} target="_blank" download>
                      <Download className="h-3 w-3 mr-1" />
                      Download
                    </a>
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Additional YouTube Embed Preview */}
        <div className="mt-6">
          <h5 className="font-medium mb-3 flex items-center space-x-2">
            <Youtube className="h-4 w-4 text-red-500" />
            <span>YouTube Embed Preview</span>
          </h5>
          <div className="aspect-video rounded-lg overflow-hidden bg-black">
            <iframe 
              src={`https://www.youtube.com/embed/${youtubeUrl.split('v=')[1]?.split('&')[0] || youtubeUrl.split('/').pop()}`}
              frameBorder="0" 
              allowFullScreen
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              className="w-full h-full"
            />
          </div>
          <div className="mt-2 text-center">
            <Button variant="outline" size="sm" asChild>
              <a href={youtubeUrl} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="h-3 w-3 mr-1" />
                Open in YouTube
              </a>
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}