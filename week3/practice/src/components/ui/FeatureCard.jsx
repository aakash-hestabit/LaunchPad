import React from "react";

const FeatureCard = ({ title, description }) => {
  return (
    <div className="feature-card bg-white p-6 rounded-lg shadow-lg text-center">
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default FeatureCard;
