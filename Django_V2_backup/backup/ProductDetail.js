import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom'; // Import useNavigate
import './ProductDetail.css'; // Optional: Create a CSS file for styling

const ProductDetail = () => {
    const { productId } = useParams(); // Get productId from URL
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate(); // Initialize navigate for routing

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

    const handleDelete = async () => {
        const confirmDelete = window.confirm("Are you sure you want to delete this product?");
        if (confirmDelete) {
            try {
                await axios.delete(`http://127.0.0.1:8000/api/products/${productId}/`);
                alert("Product deleted successfully!");
                navigate('/products'); // Redirect to the products list after deletion
            } catch (error) {
                console.error("Error deleting product:", error);
                alert("There was an error deleting the product.");
            }
        }
    };

    if (loading) {
        return <div>Loading...</div>; // Loading state
    }

    return (
        <div className="product-detail-container">
            {product ? (
                <>
                    <h2>{product.name}</h2>
                    <p><strong>ID:</strong> {product.id}</p> {/* Change product.productId to product.id */}
                    <p><strong>Price:</strong> ${Number(product.price).toFixed(2)}</p>
                    <p><strong>Rating:</strong> {product.rating ? product.rating : 'N/A'}</p>
                    <p><strong>Stock Quantity:</strong> {product.stock_quantity}</p> {/* Change product.stockQuantity to product.stock_quantity */}
                    {/* Add more details as needed */}

                    {/* Edit Product Button */}
                    <button onClick={() => navigate(`/edit-product/${productId}`)}>Edit Product</button>

                    {/* Delete Product Button */}
                    <button onClick={handleDelete} style={{ marginLeft: '10px', backgroundColor: 'red', color: 'white' }}>
                        Delete Product
                    </button>
                </>
            ) : (
                <p>Product not found.</p>
            )}
        </div>
    );
};

export default ProductDetail;
