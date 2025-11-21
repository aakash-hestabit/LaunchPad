'use client'
import React from 'react'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const AreaChart = () => {
    const data = {
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 
        datasets: [
            {
                label: '',
                data: [10000, 30000, 25000, 18000, 17000, 29000, 31000, 33000, 25000, 23000, 32000, 31000, 38000],
                fill: true,
                borderColor: 'rgb(32, 103, 185)',
                tension: 0.45,
                borderWidth: 3.5,
                backgroundColor: "blue",
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
                text: '',
            },
        },
        scales: {
            x: {
                max: 13,
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
                    stepSize: 10000,
                },
            },
        },
    }

    return (
        <Line data={data} options={options} />
    )
}

export default AreaChart
