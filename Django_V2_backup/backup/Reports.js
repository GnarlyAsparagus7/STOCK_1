import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SalesSummary = () => {
    const [salesData, setSalesData] = useState([]);

    useEffect(() => {
        const fetchSalesSummary = async () => {
            const response = await axios.get('http://127.0.0.1:8000/api/reports/sales-summary/');
            setSalesData(response.data);
        };

        fetchSalesSummary();
    }, []);

    return (
        <div>
            <h2>Sales Summary</h2>
            {/* Render your data here, e.g., in a table or chart */}
            <ul>
                {salesData.map(sale => (
                    <li key={sale.id}>{sale.product} - {sale.totalAmount}</li>
                ))}
            </ul>
            
            
        </div>
    );
};

export default SalesSummary;