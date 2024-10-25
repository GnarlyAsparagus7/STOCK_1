import React, { useState } from 'react';
import axios from 'axios';


const AddPurchase = () => {
    const [productId, setProductId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [unitCost, setUnitCost] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://127.0.0.1:8000/api/purchases/', {
                productId,
                quantity,
                unitCost,
            });
            alert('Purchase recorded successfully!');
            // Optionally reset the form or redirect
            setProductId('');
            setQuantity('');
            setUnitCost('');
        } catch (error) {
            console.error("Error recording purchase:", error);
            alert('Failed to record purchase.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Record Purchase</h2>
            <input
                type="text"
                placeholder="Product ID"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
                required
            />
            <input
                type="number"
                placeholder="Quantity"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                required
            />
            <input
                type="number"
                placeholder="Unit Cost"
                value={unitCost}
                onChange={(e) => setUnitCost(e.target.value)}
                required
            />
            <button type="submit">Add Purchase</button>
        </form>
    );
};

export default AddPurchase;