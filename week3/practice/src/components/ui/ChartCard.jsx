import React from 'react';

const ChartCard = ({ title, logo, children }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-4 mb-4">
      <div className="flex items-center mb-4">
        <div className="text-xl mr-3">{logo}</div>
        <h2 className="text-lg font-semibold">{title}</h2>
      </div>
      <div className="w-full aspect-5/3">{children}</div>
    </div>
  );
};

export default ChartCard;
