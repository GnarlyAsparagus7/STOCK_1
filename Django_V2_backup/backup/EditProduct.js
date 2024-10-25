import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const EditProduct = () => {
    const { productId } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProductDetails = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/products/${productId}/`);
                setProduct(response.data);
            } catch (error) {
                console.error("Error fetching product details:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchProductDetails();
    }, [productId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.put(`http://127.0.0.1:8000/api/products/${productId}/`, product);
            alert("Product updated successfully!");
            navigate(`/products`);
        } catch (error) {
            console.error("Error updating product:", error);
            alert("There was an error updating the product.");
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Edit Product</h2>
            <input
                type="text"
                value={product.name}
                onChange={(e) => setProduct({ ...product, name: e.target.value })}
                placeholder="Product Name"
                required
            />
            <input
                type="number"
                value={product.price}
                onChange={(e) => setProduct({ ...product, price: e.target.value })}
                placeholder="Price"
                required
            />
            <input
                type="number"
                value={product.stock_quantity}
                onChange={(e) => setProduct({ ...product, stock_quantity: e.target.value })}
                placeholder="Stock Quantity"
                required
            />
            <button type="submit">Update Product</button>
        </form>
    );
};

export default EditProduct;
