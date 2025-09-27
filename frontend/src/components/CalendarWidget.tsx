import { useState } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from './ui/button'

export function CalendarWidget() {
  const [currentDate, setCurrentDate] = useState(new Date())

  const today = new Date()
  const year = currentDate.getFullYear()
  const month = currentDate.getMonth()

  // Get first day of month and number of days
  const firstDayOfMonth = new Date(year, month, 1)
  const lastDayOfMonth = new Date(year, month + 1, 0)
  const firstDayWeekday = firstDayOfMonth.getDay()
  const daysInMonth = lastDayOfMonth.getDate()

  // Days of the week
  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  
  // Month names
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  // Sample events - in real app, this would come from props or API
  const events = {
    15: { type: 'assignment', title: 'CS Assignment Due' },
    22: { type: 'exam', title: 'Math Midterm' },
    28: { type: 'project', title: 'History Essay' }
  }

  const navigateMonth = (direction: 'prev' | 'next') => {
    setCurrentDate(prev => {
      const newDate = new Date(prev)
      if (direction === 'prev') {
        newDate.setMonth(prev.getMonth() - 1)
      } else {
        newDate.setMonth(prev.getMonth() + 1)
      }
      return newDate
    })
  }

  const isToday = (day: number) => {
    return today.getDate() === day && 
           today.getMonth() === month && 
           today.getFullYear() === year
  }

  const hasEvent = (day: number) => {
    return events[day as keyof typeof events]
  }

  const getEventColor = (day: number) => {
    const event = events[day as keyof typeof events]
    if (!event) return ''
    
    switch (event.type) {
      case 'assignment': return 'bg-blue-500'
      case 'exam': return 'bg-red-500'
      case 'project': return 'bg-green-500'
      default: return 'bg-gray-500'
    }
  }

  // Generate calendar days
  const calendarDays = []
  
  // Add empty cells for days before month starts
  for (let i = 0; i < firstDayWeekday; i++) {
    calendarDays.push(<div key={`empty-${i}`} className="h-8"></div>)
  }
  
  // Add days of the month
  for (let day = 1; day <= daysInMonth; day++) {
    calendarDays.push(
      <div
        key={day}
        className={`
          h-8 flex items-center justify-center text-sm relative cursor-pointer rounded
          ${isToday(day) 
            ? 'bg-blue-600 text-white font-semibold' 
            : 'hover:bg-gray-100'
          }
        `}
      >
        {day}
        {hasEvent(day) && (
          <div 
            className={`absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full ${getEventColor(day)}`}
            title={events[day as keyof typeof events]?.title}
          />
        )}
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          {monthNames[month]} {year}
        </h2>
        <div className="flex space-x-1">
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => navigateMonth('prev')}
            className="h-8 w-8"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => navigateMonth('next')}
            className="h-8 w-8"
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Days of week header */}
      <div className="grid grid-cols-7 gap-1 mb-2">
        {daysOfWeek.map(day => (
          <div key={day} className="h-8 flex items-center justify-center text-xs font-medium text-gray-500">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays}
      </div>

      {/* Legend */}
      <div className="mt-4 flex items-center justify-center space-x-4 text-xs text-gray-500">
        <div className="flex items-center">
          <div className="w-2 h-2 bg-blue-500 rounded-full mr-1"></div>
          Assignment
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 bg-red-500 rounded-full mr-1"></div>
          Exam
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
          Project
        </div>
      </div>
    </div>
  )
}