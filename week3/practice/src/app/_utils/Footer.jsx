import React from 'react'
import Link from 'next/link'
const Footer = () => {
    return (
        <footer className="bg-gray-800 text-white py-6 px-6 sm:px-12">
            <div className="flex flex-col sm:flex-row justify-between items-center">
                <div className="mb-4 sm:mb-0">
                    <h3 className="text-2xl font-semibold">Your Company</h3>
                    <p className="text-gray-400">SaaS Solutions for the Modern Business</p>
                </div>
                <div className="flex gap-4">

                    <Link href="/about" className="text-gray-400 hover:text-white">About</Link>
                    <>
                        <Link href="/about" className="text-gray-400 hover:text-white">Contact</Link>
                    </>
                    <Link href="/about" className="text-gray-400 hover:text-white">Privacy Policy</Link>

                </div>
            </div>
            <div className="text-center text-gray-500 mt-6">
                <p>&copy; {new Date().getFullYear()} Your Company. All Rights Reserved.</p>
            </div>
        </footer>
    )
}

export default Footer