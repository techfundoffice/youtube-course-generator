import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  Bug, 
  AlertTriangle, 
  Info, 
  Clock,
  CheckCircle,
  XCircle,
  Settings
} from 'lucide-react'

interface VideoInfo {
  mp4_video_url?: string
  mp4_download_status?: string
  mp4_file_size?: number
  run_id?: string
  source?: string
  cloudinary_url?: string
  error_details?: string
}

interface DebugInformationProps {
  videoInfo?: VideoInfo
  processingErrors?: Array<{
    step: string
    error: string
    timestamp: string
    severity: 'error' | 'warning' | 'info'
  }>
  systemStatus?: {
    database_connection: boolean
    api_services: Record<string, boolean>
    storage_services: Record<string, boolean>
  }
  className?: string
}

export default function DebugInformation({ 
  videoInfo, 
  processingErrors = [], 
  systemStatus,
  className = '' 
}: DebugInformationProps) {
  const hasVideoIssues = !videoInfo?.mp4_video_url || videoInfo.mp4_download_status !== 'completed'
  const hasErrors = processingErrors.length > 0

  if (!hasVideoIssues && !hasErrors && !systemStatus) {
    return null
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      default:
        return <Info className="h-4 w-4 text-blue-500" />
    }
  }

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case 'error':
        return <Badge variant="destructive">ERROR</Badge>
      case 'warning':
        return <Badge variant="default" className="bg-yellow-500">WARNING</Badge>
      default:
        return <Badge variant="outline">INFO</Badge>
    }
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Video Debug Information */}
      {hasVideoIssues && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Bug className="h-5 w-5" />
              <span>Video Debug Information</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Alert>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <strong>Video Processing Issues Detected</strong>
                <div className="mt-3 space-y-2 text-sm font-mono bg-muted p-3 rounded">
                  <div>
                    <span className="text-muted-foreground">mp4_video_url:</span>{' '}
                    <span className="text-foreground">"{videoInfo?.mp4_video_url || 'Not set'}"</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">mp4_download_status:</span>{' '}
                    <span className="text-foreground">"{videoInfo?.mp4_download_status || 'Not set'}"</span>
                  </div>
                  {videoInfo?.run_id && (
                    <div>
                      <span className="text-muted-foreground">run_id:</span>{' '}
                      <span className="text-foreground">"{videoInfo.run_id}"</span>
                    </div>
                  )}
                  {videoInfo?.source && (
                    <div>
                      <span className="text-muted-foreground">source:</span>{' '}
                      <span className="text-foreground">"{videoInfo.source}"</span>
                    </div>
                  )}
                  {videoInfo?.error_details && (
                    <div>
                      <span className="text-muted-foreground">error_details:</span>{' '}
                      <span className="text-red-500">"{videoInfo.error_details}"</span>
                    </div>
                  )}
                </div>
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}

      {/* Processing Errors */}
      {hasErrors && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5" />
              <span>Processing Errors & Warnings</span>
              <Badge variant="outline">{processingErrors.length} issues</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {processingErrors.map((error, index) => (
                <div key={index} className="border-l-4 border-l-red-500 pl-4 py-2">
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center space-x-2">
                      {getSeverityIcon(error.severity)}
                      <span className="font-medium">{error.step}</span>
                      {getSeverityBadge(error.severity)}
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {new Date(error.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">{error.error}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* System Status */}
      {systemStatus && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>System Status</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Database Connection */}
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Database Connection</span>
                <div className="flex items-center space-x-2">
                  {systemStatus.database_connection ? (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-500" />
                  )}
                  <Badge 
                    variant={systemStatus.database_connection ? "default" : "destructive"}
                    className={systemStatus.database_connection ? "bg-green-500" : ""}
                  >
                    {systemStatus.database_connection ? 'Connected' : 'Disconnected'}
                  </Badge>
                </div>
              </div>

              {/* API Services */}
              <div>
                <h4 className="text-sm font-medium mb-2">API Services</h4>
                <div className="space-y-2">
                  {Object.entries(systemStatus.api_services).map(([service, status]) => (
                    <div key={service} className="flex items-center justify-between text-sm">
                      <span className="capitalize">{service} API</span>
                      <div className="flex items-center space-x-2">
                        {status ? (
                          <CheckCircle className="h-3 w-3 text-green-500" />
                        ) : (
                          <XCircle className="h-3 w-3 text-red-500" />
                        )}
                        <Badge 
                          variant={status ? "outline" : "destructive"}
                          className={status ? "border-green-500 text-green-600" : ""}
                        >
                          {status ? 'Online' : 'Offline'}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Storage Services */}
              <div>
                <h4 className="text-sm font-medium mb-2">Storage Services</h4>
                <div className="space-y-2">
                  {Object.entries(systemStatus.storage_services).map(([service, status]) => (
                    <div key={service} className="flex items-center justify-between text-sm">
                      <span className="capitalize">{service} Storage</span>
                      <div className="flex items-center space-x-2">
                        {status ? (
                          <CheckCircle className="h-3 w-3 text-green-500" />
                        ) : (
                          <XCircle className="h-3 w-3 text-red-500" />
                        )}
                        <Badge 
                          variant={status ? "outline" : "destructive"}
                          className={status ? "border-green-500 text-green-600" : ""}
                        >
                          {status ? 'Available' : 'Unavailable'}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Troubleshooting Tips */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Info className="h-5 w-5" />
            <span>Troubleshooting Tips</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            {hasVideoIssues && (
              <Alert>
                <Info className="h-4 w-4" />
                <AlertDescription>
                  <strong>Video Issues:</strong> Try refreshing the page in a few minutes, or contact support if the issue persists.
                </AlertDescription>
              </Alert>
            )}
            
            <div className="text-muted-foreground">
              <p>• Check the processing logs above for detailed error information</p>
              <p>• Video downloads may take several minutes to complete</p>
              <p>• If MP4 download fails, the YouTube embed should still work</p>
              <p>• Contact support with the course ID and error details if issues persist</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}