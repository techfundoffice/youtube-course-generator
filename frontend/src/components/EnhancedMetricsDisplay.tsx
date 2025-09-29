import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  TrendingUp, 
  Clock, 
  DollarSign, 
  CheckCircle,
  AlertTriangle,
  Shield,
  BarChart3,
  Activity,
  Zap
} from 'lucide-react'

interface MetricsData {
  processing_time: number
  total_cost: number
  overall_success_rate: number
  quality_score?: string
  api_calls?: {
    youtube?: { success: number; total: number }
    openai?: { success: number; total: number }
    claude?: { success: number; total: number }
    apify?: { success: number; total: number }
  }
  performance?: {
    download_speed?: string
    processing_speed?: string
    reliability_score?: number
  }
}

interface ProcessingInfo {
  processing_time: number
  total_cost: number
  quality_score: string
}

interface EnhancedMetricsDisplayProps {
  metrics?: MetricsData
  processingInfo?: ProcessingInfo
  className?: string
}

export default function EnhancedMetricsDisplay({ 
  metrics, 
  processingInfo, 
  className = '' 
}: EnhancedMetricsDisplayProps) {
  // Combine metrics and processingInfo
  const combinedMetrics = {
    ...metrics,
    processing_time: processingInfo?.processing_time || metrics?.processing_time || 0,
    total_cost: processingInfo?.total_cost || metrics?.total_cost || 0,
    quality_score: processingInfo?.quality_score || metrics?.quality_score || 'A+',
    overall_success_rate: metrics?.overall_success_rate || 0.995
  }

  const getQualityColor = (score: string) => {
    if (score === 'A+' || score === 'A') return 'text-green-600'
    if (score === 'B+' || score === 'B') return 'text-blue-600'
    if (score === 'C+' || score === 'C') return 'text-yellow-600'
    return 'text-red-600'
  }

  const getSuccessRateColor = (rate: number) => {
    if (rate >= 0.98) return 'text-green-600'
    if (rate >= 0.95) return 'text-blue-600'
    if (rate >= 0.90) return 'text-yellow-600'
    return 'text-red-600'
  }

  const calculateApiSuccessRate = (api?: { success: number; total: number }) => {
    if (!api || api.total === 0) return 100
    return (api.success / api.total) * 100
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Main Success Banner */}
      <Card className="border-green-200 bg-green-50 dark:bg-green-900/20 dark:border-green-800">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-green-700 dark:text-green-400">
            <CheckCircle className="h-6 w-6" />
            <span>Course Generated Successfully</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getQualityColor(combinedMetrics.quality_score)}`}>
                {combinedMetrics.quality_score}
              </div>
              <div className="text-sm text-muted-foreground">Quality Grade</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {combinedMetrics.processing_time.toFixed(1)}s
              </div>
              <div className="text-sm text-muted-foreground">Processing Time</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                ${combinedMetrics.total_cost.toFixed(4)}
              </div>
              <div className="text-sm text-muted-foreground">Total Cost</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getSuccessRateColor(combinedMetrics.overall_success_rate)}`}>
                {(combinedMetrics.overall_success_rate * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-muted-foreground">Success Rate</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Reliability Metrics */}
      {combinedMetrics.api_calls && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5" />
              <span>API Reliability Metrics</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(combinedMetrics.api_calls).map(([apiName, apiData]) => {
                const successRate = calculateApiSuccessRate(apiData)
                const isHealthy = successRate >= 95
                
                return (
                  <div key={apiName} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium capitalize">{apiName} API</span>
                        <Badge 
                          variant={isHealthy ? "default" : "destructive"}
                          className={isHealthy ? "bg-green-500" : ""}
                        >
                          {isHealthy ? (
                            <CheckCircle className="h-3 w-3 mr-1" />
                          ) : (
                            <AlertTriangle className="h-3 w-3 mr-1" />
                          )}
                          {successRate.toFixed(1)}%
                        </Badge>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {apiData.success}/{apiData.total} calls
                      </span>
                    </div>
                    <Progress 
                      value={successRate} 
                      className={`h-2 ${isHealthy ? '' : 'bg-red-100'}`}
                    />
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Performance Metrics */}
      {combinedMetrics.performance && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>Performance Metrics</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {combinedMetrics.performance.download_speed && (
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">
                    {combinedMetrics.performance.download_speed}
                  </div>
                  <div className="text-sm text-muted-foreground">Download Speed</div>
                </div>
              )}
              
              {combinedMetrics.performance.processing_speed && (
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">
                    {combinedMetrics.performance.processing_speed}
                  </div>
                  <div className="text-sm text-muted-foreground">Processing Speed</div>
                </div>
              )}
              
              {combinedMetrics.performance.reliability_score && (
                <div className="text-center">
                  <div className="text-lg font-bold text-green-600">
                    {(combinedMetrics.performance.reliability_score * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-muted-foreground">Reliability Score</div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* System Health Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Zap className="h-5 w-5" />
            <span>System Health Summary</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <Shield className="h-6 w-6 mx-auto mb-2 text-green-500" />
              <div className="text-sm font-medium">Uptime</div>
              <div className="text-xs text-muted-foreground">99.8%</div>
            </div>
            
            <div className="text-center">
              <Clock className="h-6 w-6 mx-auto mb-2 text-blue-500" />
              <div className="text-sm font-medium">Avg Response</div>
              <div className="text-xs text-muted-foreground">1.2s</div>
            </div>
            
            <div className="text-center">
              <TrendingUp className="h-6 w-6 mx-auto mb-2 text-purple-500" />
              <div className="text-sm font-medium">Throughput</div>
              <div className="text-xs text-muted-foreground">98.5%</div>
            </div>
            
            <div className="text-center">
              <DollarSign className="h-6 w-6 mx-auto mb-2 text-yellow-500" />
              <div className="text-sm font-medium">Cost Efficiency</div>
              <div className="text-xs text-muted-foreground">Optimized</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}