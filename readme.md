# Smartphone Inventory Management System

The **Smartphone Inventory Management System** is a robust platform for managing, tracking, and analyzing smartphone inventory data. The system leverages **Django** as the backend and **React** for the frontend, providing a responsive, feature-rich interface for inventory management.

## Key Features

### Backend (Django)
- **Django REST Framework**: API-first architecture, enabling integration with other services.
- **Comprehensive API Endpoints** for CRUD operations:
  - `GET /api/products/`: Retrieve product listings with advanced filtering options (search by brand, model, IMEI, etc.).
  - `POST /api/products/`: Create new products with details like brand, model, serial number, purchase data, etc.
  - `PUT /api/products/<id>/`: Update existing products.
  - `DELETE /api/products/<id>/`: Remove a product from the inventory.
- **Database Models**:
  - `Smartphone`: Core model capturing essential smartphone details (e.g., brand, model, serial number, IMEI).
  - `Product`: Captures inventory-specific details.
  - `Sale` and `Purchase`: Log transactions for sales and purchases, essential for tracking financial and stock data.
- **Data Import/Export**: Import and export inventory data in CSV format for seamless data management.
- **Reports**: Generate detailed sales reports, including sales over the last 30 days with date-based aggregations.

### API Testing
- **Postman API Testing**: Comprehensive testing of all endpoints to verify CRUD operations.
- **Data Validation & Error Handling**: Built-in data validation ensures data integrity with meaningful error messages for users.

### User Authentication and Authorization
- **Role-Based Access Control**: User roles (`Admin`, `Staff`) limit access to certain actions for security and workflow efficiency.
- **User Authentication**: Secure sign-up, login, and role management through Django’s authentication framework.

### Frontend (React)
- **Dashboard UI**: Display key metrics, including inventory counts and recent sales.
- **Inventory Page**: Allows users to search and filter inventory data by IMEI, brand, model, and other parameters.
- **Theme Support**: Toggle between light and dark themes powered by Tailwind CSS.
- **Sidebar Navigation**: A collapsible sidebar with intuitive navigation links for Dashboard, Inventory, Products, etc.

### Additional Capabilities
- **IMEI Search Functionality**: Enables search by IMEI, essential for precise inventory tracking.
- **Permissions and Access Controls**: Only authorized users can access certain actions, such as deleting products.
- **Data Validation**: Validates imported CSV files to ensure correct data types and formats.
- **Reports and Analytics**: A reporting page aggregates sales and inventory data with insightful visualizations.

---

## Database Schema Improvements

### 1. Consistency in Naming Conventions
   - Ensure all tables and fields follow a consistent naming pattern (e.g., `snake_case` or `camelCase`). For example, instead of mixing `productId` and `saleId`, standardize it to either `product_id` or `productId`.

### 2. Data Types and Nullability
   - **UUID for IDs**: Replace `varchar` fields for identifiers (`productId`, `saleId`, etc.) with `UUID` data types to guarantee uniqueness and improve query performance.
   - Ensure proper use of `timestamp` fields across all transaction tables (`Sales`, `Purchases`, `Expenses`) for accurate date-time tracking.
   - Replace `varchar` for numeric fields where necessary, such as using `bigint` for fields like `category` in `ExpenseByCategory`.

### 3. Indexes for Foreign Keys
   - Add indexes to foreign keys like `productId` in the `Sales` and `Purchases` tables to improve performance on lookup queries.

### 4. Normalization
   - **Expense Category**: Move the `category` enum field in the `Expenses` table to a separate `ExpenseCategories` table for easier category management and extensibility.
   - Add a `userId` foreign key to the `Sales` and `Purchases` tables for tracking which user performed each transaction. This will help with auditing and user-specific reports.

### 5. Improving Reporting Tables
   - Ensure that tables like `SalesSummary`, `PurchaseSummary`, and `ExpenseSummary` are being updated dynamically whenever corresponding data in `Sales`, `Purchases`, and `Expenses` changes.
   - Add fields like `product_category` in `SalesSummary` and `PurchaseSummary` to make aggregated reporting by category easier.

### 6. Data Redundancy
   - Avoid redundant data storage. Store `unitCost` and `unitPrice` in a `PriceHistory` table if the product prices change over time, rather than embedding these in multiple transaction tables like `Sales` and `Purchases`.

### 7. Expanding the `Users` Table
   - Add fields for roles or permissions (e.g., `role`, `permissions`) or create a `Roles` table linked to `Users` to allow for future expansion of role-based access control.

### 8. Foreign Keys and Relationships
   - Add foreign key constraints for all relational fields. For example:
     - `productId` in `Sales` and `Purchases` should reference the `Products` table.
     - `expenseSummaryId` in `ExpenseByCategory` should reference the `ExpenseSummary` table.
   - Use cascade update/delete for maintaining referential integrity when records are updated or deleted.

### 9. Transaction Handling
   - Implement logic at the database or application level to ensure fields like `totalAmount` in `Sales` and `totalCost` in `Purchases` are always calculated automatically to avoid inconsistency in manually entered data.

### 10. Historical Data
   - For audit trails and change logs, consider adding `history` or `audit` tables for entities like `Sales`, `Purchases`, and `Products`. This will help track changes to product prices, sales, or purchases over time.

---

## Planned Enhancements

### Backend Development
- **Enhanced API Endpoints**:
  - `PATCH` Endpoint: Allow partial updates to resources, improving update efficiency.
  - User Management Endpoint: Facilitate user role management and access control.
- **Error Handling**: Refine error handling with detailed response messages for invalid data.

### Frontend Enhancements
- **Enhanced Dashboard**: Add interactive charts and graphs for visualizing sales, purchases, and inventory trends.
- **Dedicated Product Management Page**: Streamline product addition, update, and deletion workflows.
- **Real-Time Notifications**: Push notifications for low stock alerts, completed sales, and other critical updates.
- **Dynamic Sidebar Navigation**: Improved styling with collapsible sections and enhanced UX.

### User Authentication & Security
- **JWT Authentication**: Token-based authentication for secure API interaction.
- **Password Reset and Email Verification**: Enhanced security with user account recovery options.

### Future Goals
- **Real-Time Data with WebSockets**: Live inventory updates for a dynamic and responsive user experience.
- **Machine Learning for Predictive Insights**: Implement ML models to forecast stock levels and sales trends based on historical data.
- **Mobile-Responsive Design**: Ensure the system’s usability across tablets and smartphones, optimizing for mobile workflows.

---

## Installation and Setup

### Prerequisites
- **Backend**: Python 3.7+, Django, Django REST Framework
- **Frontend**: Node.js, React, Tailwind CSS
- **Database**: SQLite (for development), with options for PostgreSQL in production

### Steps
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/smartphone-inventory.git
    cd smartphone-inventory
    ```

2. **Install Backend Dependencies**:
    ```bash
    cd backend
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    ```

3. **Run the Django Development Server**:
    ```bash
    python manage.py runserver
    ```

4. **Install Frontend Dependencies**:
    ```bash
    cd ../frontend
    npm install
    npm start
    ```

5. **Access the Application**:
   - Visit `http://localhost:8000` for the backend and `http://localhost:3000` for the React frontend.

---

## Testing

- **Backend**: Use Postman or similar API tools to test endpoints.
- **Frontend**: Verify all components render and function correctly through your browser.

---

## Contributing

Contributions are welcome. Please fork the repository and create a pull request.

## License

MIT License. See `LICENSE` file for details.