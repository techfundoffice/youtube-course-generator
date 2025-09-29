import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { 
  Clock, 
  Star,
  Video,
  BookOpen,
  ChevronDown,
  Calendar,
  GraduationCap,
  CheckCircle,
  PlayCircle,
  FileText,
  Settings,
  Download,
  AlertTriangle,
  ExternalLink
} from 'lucide-react'
import { getCourse } from '@/lib/api'
import ProcessingLogs from '@/components/ProcessingLogs'
import AdvancedVideoPlayer from '@/components/AdvancedVideoPlayer'
import ExportShareActions from '@/components/ExportShareActions'
import EnhancedMetricsDisplay from '@/components/EnhancedMetricsDisplay'
import DebugInformation from '@/components/DebugInformation'
import Navigation from '@/components/Navigation'

export default function CourseResultPage() {
  const { courseId } = useParams<{ courseId: string }>()
  const [advancedOpen, setAdvancedOpen] = useState(false)
  
  const { data: course, isLoading, error } = useQuery({
    queryKey: ['course', courseId],
    queryFn: () => getCourse(courseId!),
    enabled: !!courseId,
  })
  
  // Extract video ID from YouTube URL for embed
  const getVideoId = (url?: string) => {
    if (!url) return null
    const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/)
    return match ? match[1] : null
  }
  
  const videoId = getVideoId(course?.youtube_url)
  
  // Mock processing logs for demonstration
  const mockProcessingLogs = [
    {
      timestamp: new Date().toISOString(),
      step: 'Course Generation',
      status: 'SUCCESS' as const,
      message: 'Course structure generated successfully',
      level: 'INFO' as const
    },
    {
      timestamp: new Date().toISOString(),
      step: 'MP4 Download',
      status: 'SUCCESS' as const,
      message: 'Video downloaded and processed',
      level: 'INFO' as const
    }
  ]

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="space-y-6">
            {/* Header Skeleton */}
            <div className="space-y-4">
              <div className="h-8 bg-muted animate-pulse rounded-lg w-3/4"></div>
              <div className="h-4 bg-muted animate-pulse rounded w-1/2"></div>
            </div>
            
            {/* Stats Skeleton */}
            <div className="grid md:grid-cols-3 gap-4">
              {[1, 2, 3].map((i) => (
                <Card key={i}>
                  <CardContent className="p-4">
                    <div className="h-6 bg-muted animate-pulse rounded mb-2"></div>
                    <div className="h-4 bg-muted animate-pulse rounded w-1/2"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
            
            {/* Content Skeleton */}
            <div className="h-96 bg-muted animate-pulse rounded-lg"></div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !course) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto text-center">
            <CardContent className="p-8">
              <div className="w-12 h-12 bg-destructive/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-6 h-6 text-destructive" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Course Not Found</h3>
              <p className="text-muted-foreground">The course you're looking for doesn't exist or has been removed.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  const getQualityColor = (grade: string) => {
    switch (grade?.toUpperCase()) {
      case 'A': return 'bg-green-100 text-green-800 border-green-200'
      case 'B': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'C': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'D': return 'bg-orange-100 text-orange-800 border-orange-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="space-y-6 mb-8">
          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
            <div className="space-y-2 flex-1">
              <h1 className="text-3xl lg:text-4xl font-bold tracking-tight">
                {course.title}
              </h1>
              <p className="text-lg text-muted-foreground">
                {course.description}
              </p>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  Created {new Date(course.created_at).toLocaleDateString()}
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {course.duration || 'Unknown duration'}
                </div>
              </div>
            </div>
            
            <div className="flex-shrink-0">
              <ExportShareActions 
                course={course} 
                courseId={courseId!}
                className="w-full lg:w-auto"
              />
            </div>
          </div>

          {/* Stats Tiles */}
          <div className="grid md:grid-cols-3 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Clock className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Processing Time</p>
                    <p className="text-xl font-bold">{course.processing_time || '27s'}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
                    <Star className="w-5 h-5 text-success" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Quality Grade</p>
                    <div className="flex items-center gap-2">
                      <span className="text-xl font-bold">{course.quality_score || 'B+'}</span>
                      <Badge className={getQualityColor(course.quality_score)} variant="outline">
                        High Quality
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <GraduationCap className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Course Length</p>
                    <p className="text-xl font-bold">7 Days</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Main Content - Tabbed Interface */}
        <Tabs defaultValue="video" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 lg:w-auto lg:grid-cols-3">
            <TabsTrigger value="video" className="flex items-center gap-2">
              <PlayCircle className="w-4 h-4" />
              Video
            </TabsTrigger>
            <TabsTrigger value="outline" className="flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              Course Outline
            </TabsTrigger>
            <TabsTrigger value="materials" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Materials
            </TabsTrigger>
          </TabsList>

          {/* Video Tab */}
          <TabsContent value="video" className="space-y-6">
            <AdvancedVideoPlayer
              videoInfo={{
                title: course.title,
                author: course.author || 'Unknown',
                duration: course.duration,
                mp4_video_url: course.mp4_video_path,
                mp4_download_status: course.mp4_download_status,
                cloudinary_url: course.cloudinary_url,
                thumbnail_url: course.thumbnail_url
              }}
              youtubeUrl={course.youtube_url}
              videoId={videoId}
              courseId={courseId}
            />
          </TabsContent>

          {/* Course Outline Tab */}
          <TabsContent value="outline" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5" />
                  7-Day Learning Path
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {course.content ? (
                  <div className="space-y-6">
                    {Object.entries(course.content).map(([day, content]: [string, any], index) => (
                      <div key={day} className="border rounded-lg p-4">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-semibold">
                            {index + 1}
                          </div>
                          <h3 className="text-lg font-semibold">{content.title || `Day ${index + 1}`}</h3>
                        </div>
                        <p className="text-muted-foreground mb-3">{content.description}</p>
                        {content.topics && (
                          <div className="space-y-2">
                            <h4 className="font-medium text-sm">Key Topics:</h4>
                            <ul className="text-sm text-muted-foreground space-y-1">
                              {content.topics.map((topic: string, idx: number) => (
                                <li key={idx} className="flex items-center gap-2">
                                  <CheckCircle className="w-3 h-3 text-success" />
                                  {topic}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <BookOpen className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">Course outline will appear here once generated.</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Materials Tab */}
          <TabsContent value="materials" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Course Materials & Resources
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <Video className="w-5 h-5 text-blue-600" />
                      <div>
                        <p className="font-medium">Original Video</p>
                        <p className="text-sm text-muted-foreground">YouTube source material</p>
                      </div>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => window.open(course.youtube_url, '_blank')}
                    >
                      <ExternalLink className="w-4 h-4 mr-2" />
                      View on YouTube
                    </Button>
                  </div>
                  
                  {course.mp4_video_path && (
                    <div className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <FileText className="w-5 h-5 text-green-600" />
                        <div>
                          <p className="font-medium">MP4 Download</p>
                          <p className="text-sm text-muted-foreground">Offline viewing</p>
                        </div>
                      </div>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          const downloadUrl = course.cloudinary_url || `/api/video/${course.mp4_video_path?.split('/').pop()}`
                          window.open(downloadUrl, '_blank')
                        }}
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download MP4
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Advanced Technical Section - Collapsible */}
        <Collapsible open={advancedOpen} onOpenChange={setAdvancedOpen} className="space-y-4">
          <CollapsibleTrigger asChild>
            <Button variant="ghost" className="w-full justify-between p-4 h-auto">
              <div className="flex items-center gap-2">
                <Settings className="w-4 h-4" />
                <span className="font-medium">Advanced Information & Logs</span>
              </div>
              <ChevronDown className={`w-4 h-4 transition-transform ${advancedOpen ? 'rotate-180' : ''}`} />
            </Button>
          </CollapsibleTrigger>
          
          <CollapsibleContent className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              <div className="space-y-6">
                <EnhancedMetricsDisplay 
                  course={course}
                  className="border rounded-lg"
                />
              </div>
              
              <div className="space-y-6">
                <ProcessingLogs 
                  logs={mockProcessingLogs}
                  enableRealTime={false}
                  className="max-h-96 border rounded-lg"
                />
              </div>
            </div>
            
            <DebugInformation 
              course={course}
              processingLogs={mockProcessingLogs}
              className="border rounded-lg"
            />
          </CollapsibleContent>
        </Collapsible>
      </div>
    </div>
  )
}