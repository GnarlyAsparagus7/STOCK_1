// Django_V2/frontend/src/components/ProductsList.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Papa from 'papaparse'; // For CSV parsing
import { toast, ToastContainer } from 'react-toastify'; // For notifications
import 'react-toastify/dist/ReactToastify.css'; // Import toast CSS
import './ProductsList.css';

const ProductsList = () => {
    const [products, setProducts] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');
    const [minRating, setMinRating] = useState('');

    const fetchProducts = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/products/');
            console.log('Raw API Response:', response.data); // Debug line
            
            // Transform the data if necessary
            const formattedProducts = response.data.map(product => ({
                id: product.id,
                name: product.name,
                price: product.price,
                rating: product.rating,
                stock_quantity: product.stock_quantity
            }));
            
            console.log('Formatted Products:', formattedProducts); // Debug line
            setProducts(formattedProducts);
        } catch (error) {
            console.error("Error fetching products:", error);
            toast.error("Failed to fetch products.");
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    // Function to convert data to CSV and trigger download
    const exportToCSV = () => {
        const csvData = [
            ['ID', 'Name', 'Price', 'Rating', 'Stock Quantity'],
            ...products.map(product => [
                product.id,
                product.name,
                product.price,
                product.rating || 'N/A',
                product.stock_quantity
            ])
        ];

        const csvContent = 'data:text/csv;charset=utf-8,' + csvData.map(e => e.join(",")).join("\n");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "products.csv");
        document.body.appendChild(link); // Required for FF

        link.click();
        toast.success("Exported to CSV successfully!"); // Show success toast
    };

    // Function to handle file upload
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            Papa.parse(file, {
                complete: async (results) => {
                    const productsData = results.data.slice(1); // Skip header
                    let successCount = 0;
                    let validationErrors = [];

                    for (const product of productsData) {
                        const newProduct = {
                            name: product[1],
                            price: parseFloat(product[2]),
                            rating: parseFloat(product[3]) || null,
                            stock_quantity: parseInt(product[4]),
                            user: 1  // Add the user ID here
                        };

                        if (!newProduct.name || isNaN(newProduct.price) || isNaN(newProduct.stock_quantity)) {
                            validationErrors.push(`Invalid data for product: ${newProduct.name}`);
                            continue;
                        }

                        try {
                            await axios.post('http://127.0.0.1:8000/api/products/', newProduct);
                            successCount++;
                        } catch (error) {
                            console.error("Error importing product:", error);
                            validationErrors.push(`Error importing product: ${newProduct.name}`);
                        }
                    }

                    if (validationErrors.length > 0) {
                        toast.error(`Validation Errors:\n${validationErrors.join('\n')}`);
                    }
                    if (successCount > 0) {
                        toast.success(`${successCount} products imported successfully!`);
                    }
                    fetchProducts();
                },
                header: false
            });
        }
    };

    // Filter products based on the search query and additional criteria
    const filteredProducts = products.filter(product => {
        const matchesName = product.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesPrice = (minPrice === '' || product.price >= minPrice) &&
                             (maxPrice === '' || product.price <= maxPrice);
        const matchesRating = (minRating === '' || product.rating >= minRating);
        
        return matchesName && matchesPrice && matchesRating;
    });

    return (
        <div className="products-container">
            <h2>Products</h2>
            <button className="export-button" onClick={exportToCSV}>Export to CSV</button> {/* Export button */}

            {/* Custom styled upload button */}
            <div className="upload-container">
                <label htmlFor="csvUpload" className="upload-button">
                    Upload CSV
                </label>
                <input
                    id="csvUpload"
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    style={{ display: 'none' }} // Hide default input
                />
            </div>

            <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ marginBottom: '20px', padding: '10px', width: '100%' }}
            />
            <div className="filter-container">
                <input
                    type="number"
                    placeholder="Min Price"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    style={{ marginRight: '10px', padding: '10px' }}
                />
                <input
                    type="number"
                    placeholder="Max Price"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    style={{ marginRight: '10px', padding: '10px' }}
                />
                <input
                    type="number"
                    placeholder="Min Rating"
                    value={minRating}
                    onChange={(e) => setMinRating(e.target.value)}
                    style={{ marginRight: '10px', padding: '10px' }}
                />
            </div>
            <table className="products-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Product Name</th>
                        <th>Price</th>
                        <th>Rating</th>
                        <th>Stock Quantity</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredProducts.map(product => (
                        <tr key={product.id}>
                            <td>{product.id}</td>
                            <td>
                                <Link to={`/products/${product.id}`}>{product.name}</Link>
                            </td>
                            <td>${Number(product.price).toFixed(2)}</td>
                            <td>{product.rating || 'N/A'}</td>
                            <td>{product.stock_quantity}</td>
                            <td>
                                <Link to={`/products/${product.id}`}>View</Link>
                                {" | "}
                                <Link to={`/edit-product/${product.id}`}>Edit</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <ToastContainer /> {/* Add ToastContainer to render the notifications */}
        </div>
    );
};

export default ProductsList;
