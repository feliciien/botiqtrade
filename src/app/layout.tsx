import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://boltiqtrade.vercel.app"),
  title: {
    default: "BoltIQ Trade - Trading Operations Command Center",
    template: "%s | BoltIQ Trade",
  },
  description:
    "BoltIQ Trade is the research and operations portal for BoltIQ. The primary MT5 engineering and software website is boltiqmarkets.com. No brokerage, customer deposits or custody.",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "BoltIQ Trade - Trading Operations Command Center",
    description:
      "BoltIQ Trade research and operations portal. Primary MT5 engineering and software website: boltiqmarkets.com. No customer deposits or custody.",
    url: "https://boltiqtrade.vercel.app",
    siteName: "BoltIQ Trade",
    images: [
      {
        url: "/assets/boltiq-command-center.png",
        width: 1200,
        height: 1500,
        alt: "BoltIQ command center interface for MT5, risk controls, research, and owner monitoring.",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "BoltIQ Trade",
    description:
      "Risk-first trading infrastructure for MT5 execution, auditability, and research governance.",
    images: ["/assets/boltiq-command-center.png"],
  },
  icons: {
    icon: "/assets/boltiq-mark.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  );
}
