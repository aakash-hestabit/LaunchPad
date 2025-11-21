'use client'
import React from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const BarChart = () => {
    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], // x-axis labels
        datasets: [
            {
                label: 'Monthly Data',
                data: [10000, 30000, 26000, 18000, 17000, 29000, 31000, 33000, 25000, 23000, 32000, 31000, 38000], // y-axis data points
                backgroundColor: 'rgba(32, 103, 185, 0.6)', // Color of the bars
                borderColor: 'rgb(32, 103, 185)', // Border color of the bars
                borderWidth: 1,
            },
        ],
    }

    const options = {
        responsive: true,

        plugins: {
            legend: {
                display: false,
                position: 'top',
            },
            title: {
                display: false,
                text: 'Monthly Bar Chart Example', // Title of the chart
            },
        },
        scales: {
            x: {
                grid: {
                    display: false,
                },
            },
            y: {
                min: 0,
                grid: {
                    display: true,
                },
                ticks: {
                    stepSize: 5000, // Set step size for the y-axis
                },
            },
        },
    }

    return (
        <Bar data={data} options={options} />
    )
}

export default BarChart
