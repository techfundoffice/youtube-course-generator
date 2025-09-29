import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  Activity,
  Database,
  Server,
  Zap,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign
} from 'lucide-react'
import { getSystemHealth } from '@/lib/api'

export default function DashboardPage() {
  const { data: systemHealth, isLoading, error } = useQuery({
    queryKey: ['system-health'],
    queryFn: getSystemHealth,
    refetchInterval: 30000, // Refresh every 30 seconds
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error || !systemHealth) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Failed to load system health</p>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'success':
        return 'text-green-500'
      case 'warning':
        return 'text-yellow-500'
      case 'error':
        return 'text-red-500'
      default:
        return 'text-muted-foreground'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      default:
        return <Activity className="h-4 w-4 text-muted-foreground" />
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">System Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor system health, performance, and reliability metrics
        </p>
      </div>

      {/* System Health Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="text-sm font-medium">Reliability</span>
            </div>
            <div className="text-2xl font-bold text-green-500">
              {systemHealth.system_health.reliability_percentage}%
            </div>
            <Progress value={systemHealth.system_health.reliability_percentage} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Database className="h-4 w-4 text-blue-500" />
              <span className="text-sm font-medium">Total Courses</span>
            </div>
            <div className="text-2xl font-bold">
              {systemHealth.system_health.total_courses}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-purple-500" />
              <span className="text-sm font-medium">Avg. Processing</span>
            </div>
            <div className="text-2xl font-bold">
              {systemHealth.system_health.avg_processing_time.toFixed(1)}s
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Zap className="h-4 w-4 text-yellow-500" />
              <span className="text-sm font-medium">Uptime</span>
            </div>
            <div className="text-2xl font-bold text-green-500">
              {systemHealth.system_health.uptime}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Service Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Server className="h-5 w-5" />
            <span>Service Status</span>
          </CardTitle>
          <CardDescription>
            Real-time status of all system services
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(systemHealth.services).map(([service, info]) => (
              <div key={service} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(info.status)}
                  <div>
                    <div className="font-medium capitalize">
                      {service.replace('_', ' ')}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Latency: {info.latency}
                    </div>
                  </div>
                </div>
                <Badge 
                  variant={info.status === 'success' ? 'default' : 'secondary'}
                  className={getStatusColor(info.status)}
                >
                  {info.status.toUpperCase()}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Database Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Database Statistics</span>
          </CardTitle>
          <CardDescription>
            Database performance and usage metrics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <div className="text-sm font-medium">Total Courses</div>
              <div className="text-2xl font-bold">
                {systemHealth.database.total_courses}
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="text-sm font-medium">Avg. Processing Time</div>
              <div className="text-2xl font-bold">
                {systemHealth.database.avg_processing_time.toFixed(1)}s
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="text-sm font-medium">Total Cost</div>
              <div className="text-2xl font-bold flex items-center">
                <DollarSign className="h-5 w-5 mr-1" />
                {systemHealth.database.total_cost.toFixed(2)}
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="text-sm font-medium">Connection Pool</div>
              <div className="text-2xl font-bold">
                {systemHealth.database.connection_pool_usage}
              </div>
              <Progress value={75} className="mt-2" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Performance Trends - Placeholder for charts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Performance Trends</span>
          </CardTitle>
          <CardDescription>
            System performance over time
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-muted-foreground">
            <TrendingUp className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>Performance charts will be available soon</p>
            <p className="text-sm mt-2">
              Last updated: {new Date(systemHealth.system_health.last_updated).toLocaleString()}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}