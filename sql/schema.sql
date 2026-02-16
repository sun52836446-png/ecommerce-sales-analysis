-- 启用外键约束（SQLite 必须）
PRAGMA foreign_keys = ON;

-- 1️⃣ customers 表（父表）
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(40) PRIMARY KEY,
    customer_unique_id VARCHAR(40),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(50),
    customer_state VARCHAR(10)
);

-- 2️⃣ products 表（父表）
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(40) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);

-- 3️⃣ sellers 表（父表）
CREATE TABLE IF NOT EXISTS sellers (
    seller_id VARCHAR(40) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(50),
    seller_state VARCHAR(10)
);

-- 4️⃣ category 表（维度表，可选外键）
CREATE TABLE IF NOT EXISTS category (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100)
);

-- 5️⃣ orders 表（父表 + 外键指向 customers）
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(40) PRIMARY KEY,
    customer_id VARCHAR(40),
    order_status VARCHAR(20),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 6️⃣ order_items 表（子表 + 外键指向 orders, products, sellers）
CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(40),
    order_item_id INT,
    product_id VARCHAR(40),
    seller_id VARCHAR(40),
    shipping_limit_date TIMESTAMP,
    price FLOAT,
    freight_value FLOAT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- 7️⃣ order_payments 表（子表 + 外键指向 orders）
CREATE TABLE IF NOT EXISTS order_payments (
    order_id VARCHAR(40),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value FLOAT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 8️⃣ order_reviews 表（子表 + 外键指向 orders）
CREATE TABLE IF NOT EXISTS order_reviews (
    review_id VARCHAR(40),
    order_id VARCHAR(40),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 9️⃣ geolocation 表（独立表，暂无外键）
CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city VARCHAR(50),
    geolocation_state VARCHAR(10)
);


SELECT name FROM sqlite_master
WHERE type='table';

PRAGMA table_info(orders);
PRAGMA table_info(order_items);
PRAGMA table_info(order_payments);
PRAGMA table_info(order_reviews);

PRAGMA foreign_key_list(orders);
PRAGMA foreign_key_list(order_items);
PRAGMA foreign_key_list(order_payments);
PRAGMA foreign_key_list(order_reviews);


