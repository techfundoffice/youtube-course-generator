import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider } from '@/components/theme-provider'
import { Toaster } from '@/components/ui/toaster'
import HomePage from '@/pages/HomePage'
import CourseResultPage from '@/pages/CourseResultPage'
import CoursesPage from '@/pages/CoursesPage'
import DashboardPage from '@/pages/DashboardPage'
import Navigation from '@/components/Navigation'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="dark" storageKey="course-generator-theme">
        <Router>
          <div className="min-h-screen bg-background font-sans antialiased">
            <Navigation />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/course/:courseId" element={<CourseResultPage />} />
                <Route path="/courses" element={<CoursesPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
              </Routes>
            </main>
            <Toaster />
          </div>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App