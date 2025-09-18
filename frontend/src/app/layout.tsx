import '../styles/globals.css'

export const metadata = {
  title: 'AI Influencer - Create Viral Content with AI',
  description: 'Generate stunning AI images and videos of virtual influencers to advertise and sell your products. Professional, viral-ready content in seconds.',
  keywords: 'AI influencer, AI images, AI videos, content creation, marketing, advertising',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  )
}