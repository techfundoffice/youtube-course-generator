import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  BookOpen, 
  Clock, 
  Users, 
  TrendingUp, 
  Calendar,
  ExternalLink
} from 'lucide-react'
import { getCourses } from '@/lib/api'

export default function CoursesPage() {
  const { data: courses, isLoading, error } = useQuery({
    queryKey: ['courses'],
    queryFn: getCourses,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p>Loading courses...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Failed to load courses</p>
      </div>
    )
  }

  if (!courses || courses.length === 0) {
    return (
      <div className="text-center py-12">
        <BookOpen className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
        <h2 className="text-2xl font-semibold mb-2">No courses yet</h2>
        <p className="text-muted-foreground mb-6">
          Generate your first course from a YouTube video
        </p>
        <Link to="/">
          <Button>
            Generate Course
          </Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Generated Courses</h1>
        <p className="text-muted-foreground">
          View and manage your AI-generated learning courses
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Total Courses</span>
            </div>
            <div className="text-2xl font-bold">{courses.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Avg. Processing</span>
            </div>
            <div className="text-2xl font-bold">47.9s</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Success Rate</span>
            </div>
            <div className="text-2xl font-bold">99.5%</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">This Month</span>
            </div>
            <div className="text-2xl font-bold">{courses.filter(c => 
              new Date(c.created_at).getMonth() === new Date().getMonth()
            ).length}</div>
          </CardContent>
        </Card>
      </div>

      {/* Courses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <Card key={course.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="line-clamp-2">{course.course_title}</CardTitle>
              <CardDescription className="line-clamp-3">
                {course.course_description}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Course Info */}
              <div className="flex flex-wrap gap-2">
                {course.difficulty_level && (
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <TrendingUp className="h-3 w-3" />
                    <span>{course.difficulty_level}</span>
                  </Badge>
                )}
                {course.estimated_total_time && (
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <Clock className="h-3 w-3" />
                    <span>{course.estimated_total_time}</span>
                  </Badge>
                )}
                {course.target_audience && (
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <Users className="h-3 w-3" />
                    <span>{course.target_audience}</span>
                  </Badge>
                )}
              </div>

              {/* Video Info */}
              {course.video_info && (
                <div className="text-sm text-muted-foreground">
                  <p className="font-medium">{course.video_info.title}</p>
                  <p>by {course.video_info.author}</p>
                </div>
              )}

              {/* Created Date */}
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Calendar className="h-4 w-4" />
                <span>
                  Created {new Date(course.created_at).toLocaleDateString()}
                </span>
              </div>

              {/* Actions */}
              <div className="flex justify-between items-center pt-2">
                <Link to={`/course/${course.id}`}>
                  <Button variant="outline" size="sm">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    View Course
                  </Button>
                </Link>
                
                {course.processing_info?.quality_score && (
                  <Badge 
                    variant={
                      course.processing_info.quality_score.startsWith('A') 
                        ? 'default' 
                        : 'secondary'
                    }
                  >
                    {course.processing_info.quality_score}
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}