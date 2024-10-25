import React, { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const Dashboard = () => {
    const [salesData, setSalesData] = useState({
        labels: [],
        datasets: [{
            label: 'Sales',
            data: [],
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
        }]
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/sales-report/');
                console.log('Sales data response:', response.data); // Debug log
                
                if (response.data && response.data.sales_data) {
                    setSalesData({
                        labels: response.data.sales_data.map(item => item.product__name),
                        datasets: [{
                            label: 'Sales ($)',
                            data: response.data.sales_data.map(item => item.total_sales),
                            backgroundColor: 'rgba(53, 162, 235, 0.5)',
                        }]
                    });
                }
            } catch (error) {
                console.error('Error fetching sales data:', error);
            }
        };

        fetchData();
    }, []);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Sales Data by Product'
            }
        },
        scales: {
            x: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Products'
                }
            },
            y: {
                type: 'linear',
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Sales Amount ($)'
                }
            }
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <h2>Sales Dashboard</h2>
            {salesData.labels.length > 0 ? (
                <Bar options={options} data={salesData} />
            ) : (
                <p>No sales data available</p>
            )}
        </div>
    );
};

export default Dashboard;
