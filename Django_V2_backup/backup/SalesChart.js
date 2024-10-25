// Django_V2/frontend/src/components/SalesChart.js

import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

const SalesChart = () => {
    const [salesData, setSalesData] = useState([]);

    useEffect(() => {
        const fetchSalesData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/sales-report/');
                setSalesData(response.data);
            } catch (error) {
                console.error("Error fetching sales data:", error);
            }
        };
        fetchSalesData();
    }, []);

    const data = {
        labels: salesData.map(item => item.product__name),
        datasets: [
            {
                label: 'Total Sales',
                data: salesData.map(item => item.total_sales),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    return (
        <div>
            <h2>Sales Report</h2>
            <Bar data={data} />
        </div>
    );
};

export default SalesChart;
