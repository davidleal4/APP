import { Navbar } from '@/components/Navbar'
import { Sidebar } from '@/components/Sidebar'
import { CalendarWidget } from '@/components/CalendarWidget'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, BookOpen, Calendar, Brain } from 'lucide-react'
import { useEffect, useState } from 'react'
import { gpaAPI, assignmentsAPI, classesAPI } from '@/lib/api'
import toast from 'react-hot-toast'

export default function DashboardPage() {
  const [gpa, setGpa] = useState<number | null>(null)
  const [deadlines, setDeadlines] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [classesCount, setClassesCount] = useState<number>(0)

  useEffect(() => {
    const load = async () => {
      try {
        const [gpaRes, assignmentsRes, classesRes] = await Promise.all([
          gpaAPI.calculate(),
          assignmentsAPI.getAll(),
          classesAPI.getAll(),
        ])
        setGpa(gpaRes.data.overall_gpa)
        const upcoming = (assignmentsRes.data || [])
          .filter((a: any) => a.due_date && !a.completed)
          .slice(0, 5)
        setDeadlines(upcoming)
        setClassesCount((classesRes.data || []).length)
      } catch (e: any) {
        toast.error('Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          <div className="container mx-auto px-6 py-8">
            <h1 className="text-3xl font-semibold text-gray-800 mb-8">Dashboard</h1>
            
            {/* Stats Cards */}
            <div className="grid gap-6 mb-8 md:grid-cols-2 xl:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Current GPA</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{gpa ?? '—'}</div>
                  <p className="text-xs text-muted-foreground">Current overall GPA</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Classes</CardTitle>
                  <BookOpen className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{classesCount}</div>
                  <p className="text-xs text-muted-foreground">Active classes</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Upcoming Deadlines</CardTitle>
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{deadlines.length}</div>
                  <p className="text-xs text-muted-foreground">Upcoming</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Study Streak</CardTitle>
                  <Brain className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">12</div>
                  <p className="text-xs text-muted-foreground">Days in a row</p>
                </CardContent>
              </Card>
            </div>

            {/* Main Content Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {/* Recent Assignments */}
              <Card className="col-span-2">
                <CardHeader>
                  <CardTitle>Recent Assignments</CardTitle>
                  <CardDescription>Your latest submissions and upcoming deadlines</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {loading && (
                      <div className="animate-pulse h-24 bg-gray-100 rounded" />
                    )}
                    {!loading && deadlines.map((a) => (
                      <div key={a.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{a.title}</h4>
                          <p className="text-sm text-gray-500">Due {new Date(a.due_date).toLocaleDateString()}</p>
                        </div>
                        <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full">Upcoming</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Calendar Widget */}
              <Card>
                <CardHeader>
                  <CardTitle>Calendar</CardTitle>
                  <CardDescription>Upcoming events and deadlines</CardDescription>
                </CardHeader>
                <CardContent>
                  <CalendarWidget />
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}