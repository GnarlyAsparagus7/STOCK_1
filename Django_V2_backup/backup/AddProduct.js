// src/components/AddProduct.js
import React, { useState } from 'react';
import axios from 'axios';
import './AddProduct.css';  // We'll create this CSS file

const AddProduct = () => {
    const [product, setProduct] = useState({
        name: '',
        price: '',
        rating: '',
        stock_quantity: '',
        user: 1  // Default user ID
    });

    const handleChange = (e) => {
        setProduct({ ...product, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log('Sending product data:', product);
            const response = await axios.post('http://127.0.0.1:8000/api/products/', product);
            console.log('Response:', response.data);
            alert('Product added successfully!');
            setProduct({
                name: '',
                price: '',
                rating: '',
                stock_quantity: '',
                user: 1
            });
        } catch (error) {
            console.error("Error adding product:", error.response?.data || error);
            alert('Failed to add product. Please check the console for details.');
        }
    };

    return (
        <div className="add-product-container">
            <div className="add-product-card">
                <h2>Add New Product</h2>
                <form onSubmit={handleSubmit} className="add-product-form">
                    <div className="form-group">
                        <label htmlFor="name">Product Name</label>
                        <input
                            id="name"
                            type="text"
                            name="name"
                            value={product.name}
                            onChange={handleChange}
                            required
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="price">Price</label>
                        <input
                            id="price"
                            type="number"
                            name="price"
                            value={product.price}
                            onChange={handleChange}
                            required
                            className="form-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="rating">Rating</label>
                        <input
                            id="rating"
                            type="number"
                            name="rating"
                            value={product.rating}
                            onChange={handleChange}
                            className="form-input"
                            min="0"
                            max="5"
                            step="0.1"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="stock_quantity">Stock Quantity</label>
                        <input
                            id="stock_quantity"
                            type="number"
                            name="stock_quantity"
                            value={product.stock_quantity}
                            onChange={handleChange}
                            required
                            className="form-input"
                        />
                    </div>

                    <button type="submit" className="submit-button">
                        Add Product
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddProduct;
