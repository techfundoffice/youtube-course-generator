const API_BASE_URL = 'http://localhost:5000'

export interface Course {
  id: number
  course_title: string
  course_description: string
  target_audience?: string
  difficulty_level?: string
  estimated_total_time?: string
  days?: any[]
  final_project?: string
  resources?: string[]
  assessment_criteria?: string
  youtube_url?: string
  video_id?: string
  video_info?: {
    title: string
    author: string
    duration: string
    view_count?: number
    published_at?: string
    thumbnail_url?: string
    mp4_video_url?: string
    mp4_file_size?: number
    mp4_download_status?: string
    cloudinary_url?: string
    cloudinary_public_id?: string
    cloudinary_thumbnail?: string
    cloudinary_upload_status?: string
    source?: string
  }
  processing_info?: {
    processing_time: number
    total_cost: number
    quality_score: string
  }
  created_at: string
}

export interface CourseListResponse {
  success: boolean
  courses: Course[]
}

export interface CourseResponse {
  success: boolean
  course: Course
}

export interface SystemHealthResponse {
  success: boolean
  system_health: {
    reliability_percentage: number
    total_courses: number
    avg_processing_time: number
    uptime: string
    last_updated: string
  }
  services: Record<string, { status: string; latency: string }>
  database: {
    total_courses: number
    avg_processing_time: number
    total_cost: number
    connection_pool_usage: string
    storage_usage: string
  }
}

// API functions
export const getCourses = async (): Promise<Course[]> => {
  const response = await fetch(`${API_BASE_URL}/api/courses`)
  const data: CourseListResponse = await response.json()
  
  if (!data.success) {
    throw new Error('Failed to fetch courses')
  }
  
  return data.courses
}

export const getCourse = async (courseId: string): Promise<Course> => {
  const response = await fetch(`${API_BASE_URL}/api/course/${courseId}`)
  const data: CourseResponse = await response.json()
  
  if (!data.success) {
    throw new Error('Failed to fetch course')
  }
  
  return data.course
}

export const getSystemHealth = async (): Promise<SystemHealthResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/system-health`)
  const data: SystemHealthResponse = await response.json()
  
  if (!data.success) {
    throw new Error('Failed to fetch system health')
  }
  
  return data
}

export const generateCourse = async (youtubeUrl: string) => {
  const response = await fetch(`${API_BASE_URL}/api/generate-course`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      youtube_url: youtubeUrl,
    }),
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.error || 'Failed to generate course')
  }
  
  return data
}