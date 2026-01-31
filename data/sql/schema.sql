CREATE DATABASE IF NOT EXISTS structured_DB;

USE structured_DB;

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(40) NOT NULL,
    city VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    subject VARCHAR(200) NOT NULL,
    category VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL,
    priority VARCHAR(40) NOT NULL,
    opened_at DATE NOT NULL,
    closed_at DATE NULL,
    summary TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
