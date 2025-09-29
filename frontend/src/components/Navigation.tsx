import { Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Youtube, 
  Home, 
  BookOpen, 
  BarChart3, 
  Menu,
  X
} from 'lucide-react'
import { useState } from 'react'

export default function Navigation() {
  const location = useLocation()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navItems = [
    { path: '/', label: 'Course Generator', icon: Home },
    { path: '/courses', label: 'Generated Courses', icon: BookOpen },
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-r from-purple-600 to-blue-600">
              <Youtube className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold">Course Generator</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:items-center md:space-x-6">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <Link key={item.path} to={item.path}>
                  <Button 
                    variant={isActive(item.path) ? "default" : "ghost"}
                    className="flex items-center space-x-2"
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Button>
                </Link>
              )
            })}
          </div>

          {/* Stats Badge */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            <Badge variant="secondary" className="flex items-center space-x-1">
              <span className="h-2 w-2 rounded-full bg-green-500"></span>
              <span>99.5% Reliability</span>
            </Badge>
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="border-t py-4 md:hidden">
            <div className="flex flex-col space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link key={item.path} to={item.path} onClick={() => setIsMenuOpen(false)}>
                    <Button 
                      variant={isActive(item.path) ? "default" : "ghost"}
                      className="w-full justify-start space-x-2"
                    >
                      <Icon className="h-4 w-4" />
                      <span>{item.label}</span>
                    </Button>
                  </Link>
                )
              })}
              <div className="pt-2">
                <Badge variant="secondary" className="flex items-center space-x-1">
                  <span className="h-2 w-2 rounded-full bg-green-500"></span>
                  <span>99.5% Reliability</span>
                </Badge>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}