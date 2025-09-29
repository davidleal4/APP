"use client"
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { Navbar } from '@/components/Navbar'
import { Sidebar } from '@/components/Sidebar'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { assignmentsAPI, classesAPI, flashcardsAPI } from '@/lib/api'
import toast from 'react-hot-toast'
import { FlashcardViewer } from '@/components/FlashcardViewer'

export default function ClassDetailPage() {
  const params = useParams()
  const classId = params?.id as string
  const [classData, setClassData] = useState<any | null>(null)
  const [assignments, setAssignments] = useState<any[]>([])
  const [flashcards, setFlashcards] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [genLoading, setGenLoading] = useState(false)

  useEffect(() => {
    if (!classId) return
    const load = async () => {
      try {
        const [cRes, aRes] = await Promise.all([
          classesAPI.getById(classId),
          assignmentsAPI.getAll(),
        ])
        setClassData(cRes.data)
        setAssignments((aRes.data || []).filter((a: any) => a.class_id === Number(classId)))
      } catch (e) {
        toast.error('Failed to load class')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [classId])

  const generateFlashcards = async () => {
    setGenLoading(true)
    try {
      const payload = { class_id: Number(classId), num_cards: 10 }
      const res = await flashcardsAPI.generate(payload)
      setFlashcards(res.data || [])
      toast.success('Flashcards generated')
    } catch (e) {
      toast.error('Failed to generate flashcards')
    } finally {
      setGenLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
          <div className="container mx-auto px-6 py-8">
            {loading ? (
              <div className="h-40 bg-gray-100 rounded animate-pulse" />
            ) : (
              <>
                <h1 className="text-3xl font-semibold text-gray-800 mb-6">{classData?.name}</h1>
                <div className="grid gap-6 lg:grid-cols-3">
                  <Card className="lg:col-span-2">
                    <CardHeader>
                      <CardTitle>Assignments</CardTitle>
                      <CardDescription>All assignments for this class</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {assignments.map((a) => (
                          <div key={a.id} className="flex items-center justify-between p-3 border rounded">
                            <div>
                              <div className="font-medium">{a.title}</div>
                              {a.due_date && (
                                <div className="text-sm text-gray-500">Due {new Date(a.due_date).toLocaleDateString()}</div>
                              )}
                            </div>
                            <div className="text-xs px-2 py-1 rounded bg-yellow-100 text-yellow-800">
                              {a.completed ? 'Complete' : 'Pending'}
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>AI Flashcards</CardTitle>
                      <CardDescription>Generate flashcards from class materials</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Button className="w-full" onClick={generateFlashcards} disabled={genLoading}>
                        {genLoading ? 'Generating...' : 'Generate Flashcards'}
                      </Button>
                    </CardContent>
                  </Card>
                </div>

                {flashcards.length > 0 && (
                  <Card className="mt-6">
                    <CardHeader>
                      <CardTitle>Review Flashcards</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <FlashcardViewer flashcards={flashcards.map((f:any, idx:number)=>({
                        id: String(f.id || idx),
                        question: f.question || f.prompt || 'Question',
                        answer: f.answer || 'Answer',
                        difficulty: (f.difficulty || 'medium') as any,
                      }))} />
                    </CardContent>
                  </Card>
                )}
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

