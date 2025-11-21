import React from 'react'
import Link from 'next/link';
import Hero from './_utils/Hero';
import Features from './_utils/Features';
import Testimonials from './_utils/Testimonials';
import Footer from './_utils/Footer';
const page = () => {
  return (
     <section>
      <Hero/>
      <Features/>
      <Testimonials/>
      <Footer/>
     </section>
  )
}

export default page