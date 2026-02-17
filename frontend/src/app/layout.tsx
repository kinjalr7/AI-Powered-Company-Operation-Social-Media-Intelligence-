import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AI Social Intelligence - Company Operations & Analytics",
  description: "AI-powered social media intelligence and company operations analytics platform",
  keywords: ["AI", "social media", "analytics", "intelligence", "business", "operations"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-inter bg-background text-foreground antialiased`}>
        <div className="min-h-screen">
          {children}
        </div>
        <Toaster position="top-right" richColors />
      </body>
    </html>
  );
}