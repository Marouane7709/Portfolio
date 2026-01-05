import './globals.css'
import { Inter } from 'next/font/google'
import Navigation from '@/components/Navigation'
import ParticlesBackground from '@/components/ParticlesBackground'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Portfolio',
  description: 'My professional portfolio showcasing my skills and projects',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} relative min-h-screen bg-slate-900 transition-colors duration-500`}>
        <ParticlesBackground />
        <div className="relative z-10">
          <Navigation />
          <main>
            {children}
          </main>
          <footer className="mt-20 py-8 bg-slate-900/95 backdrop-blur-lg border-t border-slate-800/50">
            <div className="container mx-auto px-4 text-center text-gray-400">
              © {new Date().getFullYear()} - Built with Next.js and Tailwind CSS
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
} 