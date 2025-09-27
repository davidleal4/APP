import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'StudyOS - Your AI Copilot for College',
  description: 'Never miss a deadline. Study smarter. Predict your GPA.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}