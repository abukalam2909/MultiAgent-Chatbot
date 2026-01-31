USE structured_DB;

INSERT INTO customers (name, email, phone, city, status, created_at) VALUES
('Abu Kalam', 'abu.kalam@gmail.com', '+1-712-562-1280', 'Toronto', 'Active', '2025-02-14'),
('John samuel', 'john.sam@yahoo.com', '+1-902-555-0198', 'Halifax', 'Active', '2023-11-02'),
('MS Dhoni', 'dhoni@bcci.com', '+1-512-555-0175', 'Calgary', 'Active', '2023-05-21'),
('Virat', 'kohli@icc.com', '+1-206-555-0104', 'Toronto', 'Inactive', '2024-07-05'),
('Steve Smith', 'smith@icc.com', '+1-512-555-0139', 'Vancouver', 'Inactive', '2022-08-18');

INSERT INTO tickets (customer_id, subject, category, status, priority, opened_at, closed_at, summary) VALUES
(1, 'Refund request for delayed shipment', 'Refunds', 'Closed', 'High', '2024-09-12', '2024-09-14', 'Customer requested a refund due to a 10-day delay. Approved after verification.'),
(1, 'Question about warranty coverage', 'Warranty', 'Closed', 'Medium', '2024-11-01', '2024-11-03', 'Asked about 2-year warranty on electronics purchase.'),
(2, 'Account access issue', 'Account', 'Open', 'High', '2025-01-05', NULL, 'Cannot access account after password reset, awaiting verification.'),
(2, 'Late delivery complaint', 'Shipping', 'Closed', 'Medium', '2024-06-21', '2024-06-25', 'Delivery arrived 5 days late, provided a credit.'),
(3, 'Subscription cancellation', 'Billing', 'Closed', 'Low', '2024-03-19', '2024-03-20', 'Cancelled subscription and confirmed final invoice.'),
(4, 'Replacement request for defective item', 'Returns', 'Open', 'Medium', '2025-01-12', NULL, 'Reported defect within 7 days, awaiting photos.'),
(5, 'Inquiry about refunds after 30 days', 'Refunds', 'Closed', 'Low', '2023-12-02', '2023-12-03', 'Asked about refund eligibility after 30 days, provided policy summary.');
