import React from "react";

const TestimonialCard = ({ text, name, title }) => {
  return (
    <div className="testimonial-card bg-white p-6 rounded-lg w-full sm:w-80 text-center">
      <div className="text-yellow-400 mb-4">
      </div>

      <p className="text-gray-600 mb-4">"{text}"</p>
      <p className="font-semibold">{name}</p>
      <p className="text-gray-500">{title}</p>
    </div>
  );
};

export default TestimonialCard;
