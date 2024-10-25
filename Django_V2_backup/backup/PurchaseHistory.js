import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PurchaseHistory = () => {
    const [purchases, setPurchases] = useState([]);

    useEffect(() => {
        const fetchPurchases = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/purchases/');
                setPurchases(response.data);
            } catch (error) {
                console.error("Error fetching purchase history:", error);
            }
        };

        fetchPurchases();
    }, []);

    return (
        <div>
            <h2>Purchase History</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Quantity</th>
                        <th>Unit Cost</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {purchases.map(purchase => (
                        <tr key={purchase.id}>
                            <td>{purchase.product}</td>
                            <td>{purchase.quantity}</td>
                            <td>${purchase.unit_cost}</td>
                            <td>{new Date(purchase.timestamp).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PurchaseHistory;