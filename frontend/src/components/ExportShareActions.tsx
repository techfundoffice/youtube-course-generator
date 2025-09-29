import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Share2, 
  Download, 
  Printer, 
  Code, 
  Copy,
  ExternalLink,
  FileJson,
  Link2
} from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'

interface Course {
  id: number
  course_title: string
  course_description: string
  [key: string]: any
}

interface ExportShareActionsProps {
  course: Course
  metrics?: any
  className?: string
}

export default function ExportShareActions({ 
  course, 
  metrics, 
  className = '' 
}: ExportShareActionsProps) {
  const [isEmbedModalOpen, setIsEmbedModalOpen] = useState(false)
  const [isCopied, setIsCopied] = useState(false)

  const courseUrl = `${window.location.origin}/courses/${course.id}`
  const embedUrl = `${courseUrl}?embed=true`
  
  const embedCode = `<iframe 
    src="${embedUrl}" 
    width="100%" 
    height="800" 
    frameborder="0" 
    style="border: 1px solid #ddd; border-radius: 8px;"
    title="YouTube Course: ${course.course_title || 'Course'}"
    allowfullscreen>
</iframe>`

  const downloadJSON = () => {
    const data = {
      course,
      metrics,
      generated_at: new Date().toISOString()
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `youtube-course-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const printCourse = () => {
    window.print()
  }

  const shareCourse = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: course.course_title,
          text: course.course_description,
          url: courseUrl
        })
      } catch (error) {
        console.log('Error sharing:', error)
        await copyToClipboard(courseUrl)
      }
    } else {
      await copyToClipboard(courseUrl)
    }
  }

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setIsCopied(true)
      setTimeout(() => setIsCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  const copyEmbedCode = async () => {
    await copyToClipboard(embedCode)
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Share2 className="h-5 w-5" />
          <span>Export & Share</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3">
          {/* Share Course */}
          <Button 
            variant="outline" 
            size="sm" 
            onClick={shareCourse}
            className="flex items-center space-x-2"
          >
            {isCopied ? (
              <>
                <Copy className="h-4 w-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Share2 className="h-4 w-4" />
                <span>Share</span>
              </>
            )}
          </Button>

          {/* Download JSON */}
          <Button 
            variant="outline" 
            size="sm" 
            onClick={downloadJSON}
            className="flex items-center space-x-2"
          >
            <FileJson className="h-4 w-4" />
            <span>Export JSON</span>
          </Button>

          {/* Print Course */}
          <Button 
            variant="outline" 
            size="sm" 
            onClick={printCourse}
            className="flex items-center space-x-2"
          >
            <Printer className="h-4 w-4" />
            <span>Print</span>
          </Button>

          {/* Embed Code */}
          <Dialog open={isEmbedModalOpen} onOpenChange={setIsEmbedModalOpen}>
            <DialogTrigger asChild>
              <Button 
                variant="outline" 
                size="sm"
                className="flex items-center space-x-2"
              >
                <Code className="h-4 w-4" />
                <span>Embed</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle className="flex items-center space-x-2">
                  <Code className="h-5 w-5" />
                  <span>Embed Course</span>
                </DialogTitle>
                <DialogDescription>
                  Copy this code to embed the course on your website or blog.
                </DialogDescription>
              </DialogHeader>
              
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Embed Code:</label>
                  <Textarea
                    value={embedCode}
                    readOnly
                    className="font-mono text-sm min-h-32"
                    onClick={(e) => e.currentTarget.select()}
                  />
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Preview URL:</label>
                  <div className="flex items-center space-x-2">
                    <code className="flex-1 px-3 py-2 bg-muted rounded text-sm">
                      {embedUrl}
                    </code>
                    <Button variant="outline" size="sm" asChild>
                      <a href={embedUrl} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </Button>
                  </div>
                </div>
              </div>
              
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsEmbedModalOpen(false)}>
                  Close
                </Button>
                <Button onClick={copyEmbedCode}>
                  <Copy className="h-4 w-4 mr-2" />
                  Copy Code
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>

        {/* Quick Links */}
        <div className="mt-4 pt-4 border-t">
          <h4 className="text-sm font-medium mb-2">Quick Links:</h4>
          <div className="space-y-1 text-sm">
            <div className="flex items-center space-x-2">
              <Link2 className="h-3 w-3" />
              <span className="text-muted-foreground">Course URL:</span>
            </div>
            <code className="text-xs bg-muted px-2 py-1 rounded block break-all">
              {courseUrl}
            </code>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}