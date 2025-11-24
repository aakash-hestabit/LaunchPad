import React from "react";
import TestimonialCard from "@/components/ui/TestimonailsCard";
const testimonialsData = [
  {
    text: "This product has revolutionized how we work. It's easy to use and extremely powerful!",
    name: "John Doe",
    title: "CEO, ExampleCorp",
  },
  {
    text: "Our team's productivity has doubled since we started using this tool. Highly recommend!",
    name: "Jane Smith",
    title: "Product Manager, TechCo",
  },
];

const Testimonials = () => {
  return (
    <section className="bg-gray-100 py-20 px-6 sm:px-12">
      <h2 className="text-3xl font-semibold text-center mb-12">
        What Our Customers Say
      </h2>

      <div className="flex flex-wrap gap-8 justify-center">
        {testimonialsData.map((item, index) => (
          <TestimonialCard
            key={index}
            text={item.text}
            name={item.name}
            title={item.title}
          />
        ))}
      </div>
    </section>
  );
};

export default Testimonials;
