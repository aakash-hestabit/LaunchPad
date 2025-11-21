'use client'
import { useState } from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "./_utils/Sidebar";
import Header from "./_utils/Header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});



export default function RootLayout({ children }) {
    const [showSidebar, setShowSidebar] = useState(false);
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased `}
      >
        <Header setShowSidebar = {setShowSidebar}/>
        <main className="flex h-full">
          {showSidebar && <Sidebar/>}
          <section className="flex-1">
            {children}
          </section>
        </main>
                  
      </body>
    </html>
  );
}
