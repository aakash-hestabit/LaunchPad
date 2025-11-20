'use client';

import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function BarChart() {
  const data = {
    labels: ["Red", "Blue", "Yellow"],
    datasets: [{
      label: 'Votes',
      data: [12, 19, 3],
      backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"]
    }]
  };

  return <Bar data={data} />;
}
