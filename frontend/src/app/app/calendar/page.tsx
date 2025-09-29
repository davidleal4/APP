import { Navbar } from '@/components/Navbar'
import { Sidebar } from '@/components/Sidebar'
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Plus, Calendar as CalendarIcon, Clock, AlertCircle } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { assignmentsAPI } from '@/lib/api'
import { format, parse, startOfWeek, getDay } from 'date-fns'
import toast from 'react-hot-toast'

export default function CalendarPage() {
  const locales = { 'en-US': require('date-fns/locale/en-US') }
  const localizer = useMemo(() => dateFnsLocalizer({
    format, parse, startOfWeek: () => startOfWeek(new Date(), { weekStartsOn: 0 }), getDay, locales,
  }), [])

  const [events, setEvents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const res = await assignmentsAPI.getAll()
        const evts = (res.data || [])
          .filter((a: any) => a.due_date)
          .map((a: any) => ({
            id: a.id,
            title: a.title,
            start: new Date(a.due_date),
            end: new Date(a.due_date),
            resource: a,
          }))
        setEvents(evts)
      } catch (e) {
        toast.error('Failed to load calendar')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'exam':
        return <AlertCircle className="h-4 w-4" />
      case 'assignment':
        return <Clock className="h-4 w-4" />
      case 'lab':
        return <CalendarIcon className="h-4 w-4" />
      default:
        return <CalendarIcon className="h-4 w-4" />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          <div className="container mx-auto px-6 py-8">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-semibold text-gray-800">Calendar</h1>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Event
              </Button>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              {/* Calendar Widget */}
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Academic Calendar</CardTitle>
                  <CardDescription>View your assignments, exams, and important dates</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-[600px] bg-white rounded">
                    <BigCalendar
                      localizer={localizer}
                      events={events}
                      startAccessor="start"
                      endAccessor="end"
                      style={{ height: '100%' }}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Upcoming Events */}
              <Card>
                <CardHeader>
                  <CardTitle>Upcoming Events</CardTitle>
                  <CardDescription>Next 7 days</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {events.slice(0,4).map((event) => (
                      <div key={event.id} className="flex items-start space-x-3 p-3 border rounded-lg">
                        <div className={`p-2 rounded-full bg-blue-100 text-blue-800`}>
                          {getTypeIcon('assignment')}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-sm">{event.title}</h4>
                          <div className="flex items-center mt-1 text-xs text-gray-500">
                            <CalendarIcon className="h-3 w-3 mr-1" />
                            {new Date(event.start).toLocaleDateString()}
                          </div>
                        </div>
                        <Badge variant="secondary" className={`text-xs bg-yellow-100 text-yellow-800`}>
                          upcoming
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Today's Schedule */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Today's Schedule</CardTitle>
                <CardDescription>Your agenda for {new Date().toLocaleDateString()}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <div className="text-blue-600 font-medium text-sm">9:00 AM</div>
                    <div className="flex-1">
                      <h4 className="font-medium">Computer Science Lecture</h4>
                      <p className="text-sm text-gray-600">CS 301 • Room 215</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div className="text-green-600 font-medium text-sm">2:00 PM</div>
                    <div className="flex-1">
                      <h4 className="font-medium">Study Group</h4>
                      <p className="text-sm text-gray-600">Calculus Review • Library</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                    <div className="text-orange-600 font-medium text-sm">4:30 PM</div>
                    <div className="flex-1">
                      <h4 className="font-medium">Assignment Work</h4>
                      <p className="text-sm text-gray-600">Data Structures Project</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}