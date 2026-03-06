-- Create database
CREATE DATABASE IF NOT EXISTS deepanshu;
USE deepanshu;

-- Create table to store user information
CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Example insert (password is hashed with bcrypt)
-- INSERT INTO login (full_name, email, password) VALUES ('John Doe', 'john@example.com', '$2a$10$...');