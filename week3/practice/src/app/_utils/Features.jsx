import React from "react";
import FeatureCard from "@/components/ui/FeatureCard";
const featuresData = [
  {
    title: "Feature 1",
    description: "Some powerful description of the feature goes here. It's easy to use.",
  },
  {
    title: "Feature 2",
    description: "Describe another great feature of the product that stands out.",
  },
  {
    title: "Feature 3",
    description: "This feature helps you increase productivity and efficiency.",
  },
];

const Features = () => {
  return (
    <section className="py-20 px-6 sm:px-12">
      <h2 className="text-3xl font-semibold text-center mb-12">Features</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {featuresData.map((item, index) => (
          <FeatureCard
            key={index}
            title={item.title}
            description={item.description}
          />
        ))}
      </div>
    </section>
  );
};

export default Features;
