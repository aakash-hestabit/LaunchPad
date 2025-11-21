'use client'
import React from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';

const Hero = () => {
    const router = useRouter();

    const handleRedirect = () => {
        router.push('/dashboard');
    };

    return (
        <section className="bg-gradient-to-r from-indigo-600 to-blue-500 text-white text-center py-20 px-6 sm:px-12 flex flex-col items-center">
            <h1 className="text-4xl sm:text-5xl font-bold leading-tight mb-4">
                The Future of SaaS Solutions
            </h1>
            <p className="text-lg mb-8">
                Build better products, grow faster, and engage your users like never before.
            </p>
            <Button 
                background="bg-blue-700" 
                title="Get Started" 
                handleClick={handleRedirect} 
            />
        </section>
    );
};

export default Hero;
