import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Terminal, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  Trash2, 
  ArrowDown, 
  RefreshCw,
  Filter,
  Brain,
  Download,
  FileText,
  Video,
  Shield,
  AlertTriangle
} from 'lucide-react'

interface LogEntry {
  timestamp: string
  step: string
  status: 'SUCCESS' | 'FAILED' | 'IN_PROGRESS' | 'WARNING' | 'RUNNING' | 'ACTIVATED'
  message: string
  level?: 'ERROR' | 'WARNING' | 'INFO'
  details?: string
}

interface ProcessingLogsProps {
  logs: LogEntry[]
  sessionId?: string
  enableRealTime?: boolean
  className?: string
}

export default function ProcessingLogs({ 
  logs: initialLogs, 
  sessionId, 
  enableRealTime = false,
  className = '' 
}: ProcessingLogsProps) {
  const [logs, setLogs] = useState<LogEntry[]>(initialLogs)
  const [autoScroll, setAutoScroll] = useState(true)
  const [filter, setFilter] = useState<'all' | 'error' | 'warning' | 'api' | 'performance'>('all')
  const logContainerRef = useRef<HTMLDivElement>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  // Real-time log fetching
  useEffect(() => {
    if (enableRealTime && sessionId) {
      const fetchLogs = async () => {
        try {
          const response = await fetch(`http://localhost:5000/api/logs/${sessionId}`)
          const data = await response.json()
          
          if (data.success && data.logs && data.logs.length > 0) {
            setLogs(data.logs)
            
            if (autoScroll && logContainerRef.current) {
              logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
            }
          }
        } catch (error) {
          console.error('Error fetching logs:', error)
        }
      }
      
      fetchLogs() // Initial fetch
      intervalRef.current = setInterval(fetchLogs, 3000) // Fetch every 3 seconds
      
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
        }
      }
    }
  }, [sessionId, enableRealTime, autoScroll])
  
  const getStepIcon = (step: string, status: string) => {
    if (step.toLowerCase().includes('mp4') || step.toLowerCase().includes('download')) {
      return <Download className="h-4 w-4" />
    }
    if (step.toLowerCase().includes('ai') || step.toLowerCase().includes('brain')) {
      return <Brain className="h-4 w-4" />
    }
    if (step.toLowerCase().includes('transcript')) {
      return <FileText className="h-4 w-4" />
    }
    if (step.toLowerCase().includes('video')) {
      return <Video className="h-4 w-4" />
    }
    if (status === 'ACTIVATED') {
      return <Shield className="h-4 w-4" />
    }
    
    return getStatusIcon(status)
  }
  
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'SUCCESS':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'FAILED':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'IN_PROGRESS':
      case 'RUNNING':
        return <Clock className="h-4 w-4 text-blue-500 animate-pulse" />
      case 'WARNING':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      case 'ACTIVATED':
        return <Shield className="h-4 w-4 text-yellow-500" />
      default:
        return <Terminal className="h-4 w-4 text-muted-foreground" />
    }
  }

  const getStatusBadge = (status: string, level?: string) => {
    if (level === 'ERROR' || status === 'FAILED') {
      return <Badge variant="destructive">FAILED</Badge>
    }
    if (level === 'WARNING' || status === 'WARNING') {
      return <Badge variant="default" className="bg-yellow-500 text-white">WARNING</Badge>
    }
    if (status === 'ACTIVATED') {
      return <Badge variant="default" className="bg-orange-500 text-white">FALLBACK</Badge>
    }
    
    switch (status) {
      case 'SUCCESS':
        return <Badge variant="default" className="bg-green-500 text-white">SUCCESS</Badge>
      case 'IN_PROGRESS':
      case 'RUNNING':
        return <Badge variant="default" className="bg-blue-500 text-white">RUNNING</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }
  
  const getLogLevel = (log: LogEntry) => {
    if (log.level === 'ERROR' || log.status === 'FAILED') return 'text-red-500'
    if (log.level === 'WARNING' || log.status === 'WARNING') return 'text-yellow-500'
    if (log.status === 'SUCCESS') return 'text-green-500'
    if (log.status === 'RUNNING' || log.status === 'IN_PROGRESS') return 'text-blue-500'
    if (log.status === 'ACTIVATED') return 'text-orange-500'
    return 'text-gray-500'
  }
  
  const filteredLogs = logs.filter(log => {
    switch (filter) {
      case 'error':
        return log.level === 'ERROR' || log.status === 'FAILED'
      case 'warning':
        return log.level === 'WARNING' || log.status === 'WARNING'
      case 'api':
        return log.step.toLowerCase().includes('api') || 
               log.step.toLowerCase().includes('download') || 
               log.step.toLowerCase().includes('upload')
      case 'performance':
        return log.step.toLowerCase().includes('performance') || 
               log.step.toLowerCase().includes('duration') || 
               log.step.toLowerCase().includes('speed')
      default:
        return true
    }
  })
  
  const logStats = {
    total: logs.length,
    success: logs.filter(log => log.status === 'SUCCESS').length,
    errors: logs.filter(log => log.level === 'ERROR' || log.status === 'FAILED').length,
    warnings: logs.filter(log => log.level === 'WARNING' || log.status === 'WARNING').length,
    fallbacks: logs.filter(log => log.status === 'ACTIVATED').length
  }
  
  const clearLogs = () => {
    if (confirm('Clear all processing logs?')) {
      setLogs([])
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }
  
  const toggleAutoScroll = () => {
    setAutoScroll(!autoScroll)
    if (!autoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }
  
  const refreshLogs = async () => {
    if (sessionId) {
      try {
        const response = await fetch(`http://localhost:5000/api/logs/${sessionId}`)
        const data = await response.json()
        
        if (data.success && data.logs) {
          setLogs(data.logs)
        }
      } catch (error) {
        console.error('Error refreshing logs:', error)
      }
    }
  }

  if (logs.length === 0) {
    return (
      <Card className={className}>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center space-x-2">
            <Terminal className="h-5 w-5" />
            <span>Processing Output Logs</span>
          </CardTitle>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" onClick={clearLogs}>
              <Trash2 className="h-4 w-4 mr-1" />
              Clear
            </Button>
            <Button variant="outline" size="sm" onClick={toggleAutoScroll}>
              <ArrowDown className="h-4 w-4 mr-1" />
              Auto-scroll
            </Button>
            <Button variant="outline" size="sm" onClick={refreshLogs}>
              <RefreshCw className="h-4 w-4 mr-1" />
              Refresh
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto">
            <div className="text-gray-400 mb-3">
              <Terminal className="inline h-4 w-4 mr-2" />
              Real-time processing logs from course generation:
            </div>
            <div className="text-center text-gray-500 py-8">
              <Terminal className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>{enableRealTime ? 'Waiting for processing logs...' : 'No processing logs available for this session'}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center space-x-2">
          <Terminal className="h-5 w-5" />
          <span>Processing Output Logs</span>
        </CardTitle>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={clearLogs}>
            <Trash2 className="h-4 w-4 mr-1" />
            Clear
          </Button>
          <Button 
            variant={autoScroll ? "outline" : "default"} 
            size="sm" 
            onClick={toggleAutoScroll}
            className={autoScroll ? '' : 'bg-yellow-500 hover:bg-yellow-600'}
          >
            {autoScroll ? (
              <>
                <ArrowDown className="h-4 w-4 mr-1" />
                Auto-scroll
              </>
            ) : (
              <>
                <AlertTriangle className="h-4 w-4 mr-1" />
                Paused
              </>
            )}
          </Button>
          <Button variant="outline" size="sm" onClick={refreshLogs}>
            <RefreshCw className="h-4 w-4 mr-1" />
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        {/* Log Summary */}
        <div className="bg-gray-800 text-gray-100 p-3 border-b">
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-400">Processing Summary:</span>
            <div className="flex space-x-2">
              <Badge variant="default" className="bg-green-600">{logStats.success} Success</Badge>
              <Badge variant="default" className="bg-yellow-600">{logStats.warnings} Warnings</Badge>
              <Badge variant="default" className="bg-red-600">{logStats.errors} Errors</Badge>
              {logStats.fallbacks > 0 && (
                <Badge variant="default" className="bg-orange-600">{logStats.fallbacks} Fallbacks</Badge>
              )}
            </div>
          </div>
        </div>
        
        {/* Filter Buttons */}
        <div className="bg-gray-800 p-3 border-b">
          <div className="flex space-x-1">
            {['all', 'error', 'warning', 'api', 'performance'].map(filterType => (
              <Button
                key={filterType}
                variant={filter === filterType ? "default" : "outline"}
                size="sm"
                onClick={() => setFilter(filterType as typeof filter)}
                className="text-xs"
              >
                {filterType === 'all' ? 'All' :
                 filterType === 'error' ? 'Errors' :
                 filterType === 'warning' ? 'Warnings' :
                 filterType === 'api' ? 'APIs' : 'Performance'}
              </Button>
            ))}
          </div>
        </div>
        
        {/* Logs Container */}
        <div 
          ref={logContainerRef}
          className="bg-gray-900 text-gray-100 p-4 font-mono text-sm max-h-96 overflow-y-auto"
        >
          <div className="text-gray-400 mb-3">
            <Terminal className="inline h-4 w-4 mr-2" />
            Real-time processing logs from course generation:
          </div>
          
          <div className="space-y-2">
            {filteredLogs.map((log, index) => {
              const timestamp = new Date(log.timestamp).toLocaleTimeString()
              const [mainMessage, metadata] = log.details ? log.details.split('|') : [log.message || '', '']
              
              return (
                <div 
                  key={index} 
                  className={`log-entry p-2 border-l-4 ${getLogLevel(log)} border-l-current`}
                  data-step={log.step}
                  data-level={log.level}
                >
                  <div className="flex justify-between items-start mb-1">
                    <div className="flex items-center space-x-2">
                      <strong className="text-white">{log.step}</strong>
                      {getStatusBadge(log.status, log.level)}
                      {(log.level === 'ERROR' || log.status === 'FAILED') && (
                        <AlertTriangle className="h-4 w-4 text-red-500" />
                      )}
                      {log.status === 'ACTIVATED' && (
                        <Shield className="h-4 w-4 text-yellow-500" />
                      )}
                    </div>
                    <span className="text-xs text-gray-400">{timestamp}</span>
                  </div>
                  <div className="text-gray-300">{mainMessage.trim()}</div>
                  {metadata && (
                    <div className="text-xs text-gray-500 font-mono mt-1">{metadata.trim()}</div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}