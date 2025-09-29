import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { useToast } from '@/hooks/use-toast'
import { 
  Youtube, 
  Sparkles, 
  Loader2,
  Clock,
  Shield,
  CheckCircle,
  ArrowRight
} from 'lucide-react'
import ProcessingLogs from '@/components/ProcessingLogs'
import { useCourseGeneration } from '@/hooks/use-course-generation'

export default function HomePage() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const {
    generateCourse,
    isLoading,
    progress,
    currentStep,
    logs,
    error
  } = useCourseGeneration()

  const validateUrl = (url: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/
    return youtubeRegex.test(url)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!youtubeUrl) {
      toast({
        title: "URL Required",
        description: "Please enter a YouTube video URL to get started.",
        variant: "destructive"
      })
      return
    }

    if (!validateUrl(youtubeUrl)) {
      toast({
        title: "Invalid URL",
        description: "Please enter a valid YouTube URL (e.g., https://youtube.com/watch?v=...)",
        variant: "destructive"
      })
      return
    }

    try {
      const result = await generateCourse(youtubeUrl)
      if (result?.course_id) {
        navigate(`/course/${result.course_id}`)
      }
    } catch (err) {
      toast({
        title: "Generation Failed",
        description: "Unable to generate course. Please try again or contact support.",
        variant: "destructive"
      })
    }
  }

  const features = [
    {
      icon: Clock,
      title: 'Fast Processing',
      description: 'Generate courses in under 30 seconds'
    },
    {
      icon: Shield,
      title: '99.5% Reliability',
      description: 'Multi-layer redundancy ensures success'
    },
    {
      icon: Sparkles,
      title: 'AI-Powered',
      description: 'Advanced AI creates structured learning paths'
    }
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 lg:py-24">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left Column - Hero Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-5xl font-bold tracking-tight">
                Transform YouTube Videos into
                <span className="text-primary"> 7-Day Courses</span>
              </h1>
              <p className="text-xl text-muted-foreground leading-relaxed">
                Our AI-powered platform converts any YouTube video into a structured, 
                comprehensive learning course in seconds. Perfect for educators, 
                students, and lifelong learners.
              </p>
            </div>

            {/* URL Input Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="url"
                  placeholder="Paste YouTube URL here (e.g., https://youtube.com/watch?v=...)"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  className="h-14 text-lg px-6 border-2 focus:border-primary"
                  disabled={isLoading}
                  required
                />
                {youtubeUrl && !validateUrl(youtubeUrl) && (
                  <p className="text-sm text-destructive">
                    Please enter a valid YouTube URL
                  </p>
                )}
              </div>
              
              <Button 
                type="submit" 
                size="lg" 
                className="w-full h-14 text-lg font-semibold"
                disabled={isLoading || !youtubeUrl}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Creating Course...
                  </>
                ) : (
                  <>
                    Generate Course
                    <ArrowRight className="w-5 h-5 ml-2" />
                  </>
                )}
              </Button>
            </form>

            {/* Progress Indicator */}
            {isLoading && (
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Processing: {currentStep}</span>
                  <span className="font-medium">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            {/* Trust Indicators */}
            <div className="pt-4">
              <div className="flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span>99.5% Success Rate</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span>30s Average Processing</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <span>AI-Powered Analysis</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Preview Card */}
          <div className="lg:pl-8">
            <Card className="border-2 shadow-xl">
              <CardContent className="p-6">
                <div className="space-y-6">
                  <div className="flex items-center gap-3">
                    <Youtube className="w-8 h-8 text-red-500" />
                    <div>
                      <h3 className="font-semibold">Sample Course Preview</h3>
                      <p className="text-sm text-muted-foreground">7-Day Learning Path</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    {[
                      'Day 1: Introduction & Foundation',
                      'Day 2: Core Concepts',
                      'Day 3: Practical Applications',
                      'Day 4: Advanced Techniques',
                      'Day 5: Real-world Examples',
                      'Day 6: Best Practices',
                      'Day 7: Summary & Next Steps'
                    ].map((day, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg">
                        <div className="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-semibold">
                          {index + 1}
                        </div>
                        <span className="text-sm font-medium">{day}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-muted/30 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Why Choose Our Platform?</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Experience the future of learning with our advanced AI technology
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <Card key={index} className="text-center border-0 shadow-lg">
                  <CardContent className="p-8">
                    <Icon className="w-12 h-12 text-primary mx-auto mb-4" />
                    <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </div>

      {/* Processing Logs - Only show when processing */}
      {isLoading && logs.length > 0 && (
        <div className="container mx-auto px-4 pb-16">
          <ProcessingLogs 
            logs={logs} 
            enableRealTime={true} 
            className="max-h-96"
          />
        </div>
      )}
    </div>
  )
}