import './globals.css'
import { ReactNode } from 'react'
import { Analytics } from '@vercel/analytics/next'

export const metadata = {
  title: 'BoltiqTrade',
  description: 'AI-powered trading assistant for BTC/USD & EUR/USD',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
