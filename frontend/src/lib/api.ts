import axios from 'axios'
import { getSession } from 'next-auth/react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance
export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token (from localStorage fallback)
api.interceptors.request.use(async (config) => {
  if (typeof window !== 'undefined') {
    // Prefer NextAuth session token
    const session = await getSession()
    const token = (session as any)?.accessToken || localStorage.getItem('access_token')
    if (token) {
      ;(config.headers as any).Authorization = `Bearer ${token}`
    }
  }
  return config
}, (error) => Promise.reject(error))

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('access_token')
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

// Auth API calls
export const authAPI = {
  login: (email: string, password: string) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  
  register: (email: string, password: string, full_name: string) =>
    api.post('/auth/register', { email, password, full_name }),
}

// Classes API calls
export const classesAPI = {
  getAll: () => api.get('/classes/'),
  getById: (id: string) => api.get(`/classes/${id}`),
  create: (data: any) => api.post('/classes/', data),
  update: (id: string, data: any) => api.put(`/classes/${id}`, data),
  delete: (id: string) => api.delete(`/classes/${id}`),
}

// Assignments API calls
export const assignmentsAPI = {
  getAll: () => api.get('/assignments/'),
  getById: (id: string) => api.get(`/assignments/${id}`),
  create: (data: any) => api.post('/assignments/', data),
  update: (id: string, data: any) => api.put(`/assignments/${id}`, data),
  delete: (id: string) => api.delete(`/assignments/${id}`),
}

// Flashcards API calls
export const flashcardsAPI = {
  getAll: () => api.get('/flashcards/'),
  getById: (id: string) => api.get(`/flashcards/${id}`),
  create: (data: any) => api.post('/flashcards/', data),
  update: (id: string, data: any) => api.put(`/flashcards/${id}`, data),
  delete: (id: string) => api.delete(`/flashcards/${id}`),
  generate: (payload: any) => api.post('/flashcards/generate', payload),
}

// GPA API calls
export const gpaAPI = {
  calculate: () => api.get('/gpa/calculate'),
  predict: (targetGPA?: number) => 
    api.get(`/gpa/predict${targetGPA ? `?target_gpa=${targetGPA}` : ''}`),
}

export default api