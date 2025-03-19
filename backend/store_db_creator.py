
import sqlite3
import os

db_path = db_path = os.path.join(os.path.dirname(__file__), "Chinook.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.executescript('''
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS discounts;

-- Customers Table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    city TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    supplier_id INTEGER,
    price REAL NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Orders Table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')) DEFAULT 'Pending',
    total_amount REAL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table (Many-to-Many Relationship)
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    price_per_unit REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Payments Table
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    payment_method TEXT CHECK(payment_method IN ('Credit Card', 'PayPal', 'Bank Transfer', 'Cash')),
    amount REAL NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Shipments Table
CREATE TABLE shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    tracking_number TEXT,
    shipment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP,
    carrier TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Categories Table
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
);

-- Suppliers Table
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_name TEXT,
    phone TEXT,
    email TEXT UNIQUE,
    city TEXT
);

-- Employees Table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT,
    hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews Table
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Inventory Table
CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    stock_quantity INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Discounts Table
CREATE TABLE discounts (
    discount_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    discount_percentage REAL CHECK(discount_percentage BETWEEN 0 AND 100),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
''')

# Insert sample data for Customers
customers_data = [
    ("Alice Johnson", "alice@example.com", "555-1234", "New York"),
    ("Bob Smith", "bob@example.com", "555-5678", "Los Angeles"),
    ("Charlie Brown", "charlie@example.com", "555-8765", "Chicago")
]
cursor.executemany("INSERT INTO customers (name, email, phone, city) VALUES (?, ?, ?, ?)", customers_data)

# Insert sample data for Categories
categories_data = [("Electronics",), ("Appliances",), ("Furniture",), ("Clothing",), ("Books",)]
cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", categories_data)

# Insert sample data for Suppliers
suppliers_data = [
    ("TechCorp", "John Doe", "555-1111", "techcorp@example.com", "San Francisco"),
    ("HomeGoods", "Jane Doe", "555-2222", "homegoods@example.com", "Seattle")
]
cursor.executemany("INSERT INTO suppliers (name, contact_name, phone, email, city) VALUES (?, ?, ?, ?, ?)", suppliers_data)

# Insert sample data for Products
products_data = [
    ("Laptop", 1, 1, 999.99, 50),
    ("Smartphone", 1, 1, 699.99, 100),
    ("Coffee Maker", 2, 2, 79.99, 30),
    ("Desk Chair", 3, 2, 199.99, 25)
]
cursor.executemany("INSERT INTO products (name, category_id, supplier_id, price, stock_quantity) VALUES (?, ?, ?, ?, ?)", products_data)

# Insert sample data for Orders
orders_data = [
    (1, "2024-03-01 10:15:00", "Pending", 999.99),
    (2, "2024-03-02 12:30:00", "Shipped", 699.99),
    (3, "2024-03-03 15:45:00", "Delivered", 79.99)
]
cursor.executemany("INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)", orders_data)

# Insert sample data for Order Items
order_items_data = [
    (1, 1, 1, 999.99),  # Order 1 - Laptop
    (2, 2, 1, 699.99),  # Order 2 - Smartphone
    (3, 3, 1, 79.99)    # Order 3 - Coffee Maker
]
cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)", order_items_data)

# Insert sample data for Payments
payments_data = [
    (1, "Credit Card", 999.99, "2024-03-01 11:00:00"),
    (2, "PayPal", 699.99, "2024-03-02 13:00:00")
]
cursor.executemany("INSERT INTO payments (order_id, payment_method, amount, payment_date) VALUES (?, ?, ?, ?)", payments_data)

# Insert sample data for Shipments
shipments_data = [
    (2, "TRK123456", "2024-03-02 14:00:00", "2024-03-05 10:00:00", "FedEx")
]
cursor.executemany("INSERT INTO shipments (order_id, tracking_number, shipment_date, delivery_date, carrier) VALUES (?, ?, ?, ?, ?)", shipments_data)

# Insert sample data for Employees
employees_data = [
    ("David Miller", "Manager", "2020-05-10"),
    ("Emma Davis", "Sales Representative", "2021-08-15")
]
cursor.executemany("INSERT INTO employees (name, position, hire_date) VALUES (?, ?, ?)", employees_data)

# Insert sample data for Reviews
reviews_data = [
    (1, 1, 5, "Great laptop!", "2024-03-06 10:00:00"),
    (2, 2, 4, "Good phone, but battery life could be better.", "2024-03-07 12:30:00")
]
cursor.executemany("INSERT INTO reviews (customer_id, product_id, rating, comment, review_date) VALUES (?, ?, ?, ?, ?)", reviews_data)

# Commit and close
conn.commit()
conn.close()

# Provide the updated database file
db_path
