import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { X, ArrowRight, ArrowLeft } from 'lucide-react'

interface TutorialStep {
  id: string
  title: string
  content: string
  targetElement?: string
  position?: 'top' | 'bottom' | 'left' | 'right'
}

interface TutorialOverlayProps {
  steps: TutorialStep[]
  isVisible: boolean
  onComplete: () => void
  onSkip: () => void
}

export function TutorialOverlay({ steps, isVisible, onComplete, onSkip }: TutorialOverlayProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (!isVisible) {
      setCurrentStep(0)
    }
  }, [isVisible])

  if (!isVisible || steps.length === 0) {
    return null
  }

  const currentStepData = steps[currentStep]
  const isFirstStep = currentStep === 0
  const isLastStep = currentStep === steps.length - 1

  const handleNext = () => {
    if (isLastStep) {
      onComplete()
    } else {
      setIsAnimating(true)
      setTimeout(() => {
        setCurrentStep(prev => prev + 1)
        setIsAnimating(false)
      }, 150)
    }
  }

  const handlePrevious = () => {
    if (!isFirstStep) {
      setIsAnimating(true)
      setTimeout(() => {
        setCurrentStep(prev => prev - 1)
        setIsAnimating(false)
      }, 150)
    }
  }

  const handleSkip = () => {
    onSkip()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black bg-opacity-50" />
      
      {/* Tutorial Card */}
      <Card className={`relative z-10 max-w-md mx-4 transition-all duration-300 ${isAnimating ? 'scale-95 opacity-50' : 'scale-100 opacity-100'}`}>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="text-sm text-gray-500">
                Step {currentStep + 1} of {steps.length}
              </div>
              <div className="flex space-x-1">
                {steps.map((_, index) => (
                  <div
                    key={index}
                    className={`h-2 w-2 rounded-full transition-colors ${
                      index === currentStep 
                        ? 'bg-blue-500' 
                        : index < currentStep 
                        ? 'bg-blue-300' 
                        : 'bg-gray-200'
                    }`}
                  />
                ))}
              </div>
            </div>
            <Button variant="ghost" size="icon" onClick={handleSkip}>
              <X className="h-4 w-4" />
            </Button>
          </div>
          <CardTitle className="text-lg">{currentStepData.title}</CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <p className="text-gray-600">{currentStepData.content}</p>
          
          <div className="flex items-center justify-between">
            <Button 
              variant="outline" 
              onClick={handlePrevious}
              disabled={isFirstStep}
              className="flex items-center"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Previous
            </Button>
            
            <div className="flex space-x-2">
              <Button variant="ghost" onClick={handleSkip}>
                Skip Tour
              </Button>
              <Button onClick={handleNext} className="flex items-center">
                {isLastStep ? 'Finish' : 'Next'}
                {!isLastStep && <ArrowRight className="h-4 w-4 ml-2" />}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Highlight target element if specified */}
      {currentStepData.targetElement && (
        <div className="absolute inset-0 pointer-events-none">
          <div 
            className="absolute border-2 border-blue-500 rounded-lg bg-blue-500 bg-opacity-10 animate-pulse"
            style={{
              // In a real implementation, you'd calculate the position of the target element
              // For now, this is just a placeholder
              top: '20%',
              left: '20%',
              width: '200px',
              height: '100px'
            }}
          />
        </div>
      )}
    </div>
  )
}

// Predefined tutorial steps for different pages
export const dashboardTutorialSteps: TutorialStep[] = [
  {
    id: 'welcome',
    title: 'Welcome to StudyApp!',
    content: 'Let\'s take a quick tour of your dashboard to help you get started with managing your academic life.'
  },
  {
    id: 'stats',
    title: 'Your Academic Stats',
    content: 'These cards show your current GPA, active classes, upcoming deadlines, and study streak. They update automatically as you add assignments and classes.',
    targetElement: 'stats-cards'
  },
  {
    id: 'assignments',
    title: 'Recent Assignments',
    content: 'View your latest assignments here. You can see their status, due dates, and priority levels at a glance.',
    targetElement: 'recent-assignments'
  },
  {
    id: 'calendar',
    title: 'Calendar Widget',
    content: 'The calendar shows your upcoming events and deadlines. Click on any date to see more details or add new events.',
    targetElement: 'calendar-widget'
  },
  {
    id: 'navigation',
    title: 'Navigation Menu',
    content: 'Use the sidebar to navigate between different sections: Classes, Calendar, Flashcards, Projects, and GPA tracking.',
    targetElement: 'sidebar'
  }
]

export const classesTutorialSteps: TutorialStep[] = [
  {
    id: 'classes-intro',
    title: 'Managing Your Classes',
    content: 'This is where you can view and manage all your classes for the current semester.'
  },
  {
    id: 'add-class',
    title: 'Adding a New Class',
    content: 'Click the "Add Class" button to create a new class. Include details like course name, code, professor, and credits.',
    targetElement: 'add-class-button'
  },
  {
    id: 'class-details',
    title: 'Class Details',
    content: 'Click on any class to view detailed information, assignments, and track your progress in that course.'
  }
]

export const calendarTutorialSteps: TutorialStep[] = [
  {
    id: 'calendar-intro',
    title: 'Your Academic Calendar',
    content: 'Stay organized with a visual overview of all your assignments, exams, and important dates.'
  },
  {
    id: 'upcoming-events',
    title: 'Upcoming Events',
    content: 'The sidebar shows your next upcoming events with priority indicators to help you focus on what\'s most urgent.',
    targetElement: 'upcoming-events'
  },
  {
    id: 'add-event',
    title: 'Adding Events',
    content: 'Create custom events, set reminders, and organize your study schedule using the "Add Event" button.',
    targetElement: 'add-event-button'
  }
]