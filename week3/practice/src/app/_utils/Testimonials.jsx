import React from 'react'
import {  FaStar } from "react-icons/fa";

const Testimonials = () => {
  return (
    <section className="bg-gray-100 py-20 px-6 sm:px-12">
        <h2 className="text-3xl font-semibold text-center mb-12">What Our Customers Say</h2>
        <div className="flex flex-wrap gap-8 justify-center">
          <div className="testimonial-card bg-white p-6 rounded-lg shadow-lg w-full sm:w-80 text-center">
            <div className="text-yellow-400 mb-4">
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
            </div>
            <p className="text-gray-600 mb-4">
              "This product has revolutionized how we work. It's easy to use and extremely powerful!"
            </p>
            <p className="font-semibold">John Doe</p>
            <p className="text-gray-500">CEO, ExampleCorp</p>
          </div>
          <div className="testimonial-card bg-white p-6 rounded-lg shadow-lg w-full sm:w-80 text-center">
            <div className="text-yellow-400 mb-4">
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
              <FaStar className="inline" />
            </div>
            <p className="text-gray-600 mb-4">
              "Our team's productivity has doubled since we started using this tool. Highly recommend!"
            </p>
            <p className="font-semibold">Jane Smith</p>
            <p className="text-gray-500">Product Manager, TechCo</p>
          </div>
        </div>
      </section>
  )
}

export default Testimonials