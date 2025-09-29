import { useState, useCallback } from 'react'
import { useToast } from '@/hooks/use-toast'
import { io } from 'socket.io-client'

interface LogEntry {
  timestamp: string
  step: string
  status: 'SUCCESS' | 'FAILED' | 'IN_PROGRESS' | 'WARNING'
  message: string
  level?: string
}

interface CourseGenerationResult {
  success: boolean
  course_id?: number
  error?: string
}

export const useCourseGeneration = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState(0)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const generateCourse = useCallback(async (youtubeUrl: string): Promise<CourseGenerationResult | null> => {
    setIsLoading(true)
    setProgress(0)
    setCurrentStep(0)
    setLogs([])
    setError(null)

    try {
      // Connect to Socket.io for real-time updates
      const socket = io('http://localhost:5000')

      // Listen for progress updates
      socket.on('progress_update', (data) => {
        setProgress(data.progress || 0)
        setCurrentStep(data.step_index || 0)
        
        // Add log entry
        const logEntry: LogEntry = {
          timestamp: new Date().toISOString(),
          step: data.step || 'Processing',
          status: data.status || 'IN_PROGRESS',
          message: data.message || 'Processing...',
          level: data.level || 'INFO'
        }
        
        setLogs(prev => [...prev, logEntry])
      })

      // Listen for completion
      socket.on('course_complete', (data) => {
        setProgress(100)
        setCurrentStep(3)
        socket.disconnect()
      })

      // Listen for errors
      socket.on('error', (data) => {
        setError(data.message || 'An error occurred')
        socket.disconnect()
      })

      // Make API call to generate course
      const response = await fetch('http://localhost:5000/api/generate-course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          youtube_url: youtubeUrl,
        }),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.error || 'Failed to generate course')
      }

      if (result.success) {
        toast({
          title: "Success!",
          description: "Course generated successfully",
        })
        
        socket.disconnect()
        return result
      } else {
        throw new Error(result.error || 'Course generation failed')
      }

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred'
      setError(errorMessage)
      
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive"
      })
      
      return null
    } finally {
      setIsLoading(false)
    }
  }, [toast])

  return {
    generateCourse,
    isLoading,
    progress,
    currentStep,
    logs,
    error
  }
}