INSERT INTO users (role, username, hashed_password, email, dob, code, expiry, refresh_token, last_login)
VALUES
    ('user', 'user1', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user1@example.com', '1995-02-02', 'code2', '2025-02-02', 'refresh_token_2', '2024-04-18 13:00:00'),
    ('user', 'user2', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user2@example.com', '1998-03-03', 'code3', '2025-03-03', 'refresh_token_3', '2024-04-18 14:00:00'),
    ('user', 'user3', 'hashed$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u_password_4', 'user3@example.com', '1988-04-04', 'code4', '2025-04-04', 'refresh_token_4', '2024-04-18 15:00:00'),
    ('user', 'user4', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user4@example.com', '1992-05-05', 'code5', '2025-05-05', 'refresh_token_5', '2024-04-18 16:00:00'),
    ('user', 'user5', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user5@example.com', '1994-06-06', 'code6', '2025-06-06', 'refresh_token_6', '2024-04-18 17:00:00'),
    ('user', 'user6', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user6@example.com', '1991-07-07', 'code7', '2025-07-07', 'refresh_token_7', '2024-04-18 18:00:00'),
    ('user', 'user7', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user7@example.com', '1996-08-08', 'code8', '2025-08-08', 'refresh_token_8', '2024-04-18 19:00:00'),
    ('staff', 'user8', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'user8@example.com', '1989-09-09', 'code9', '2025-09-09', 'refresh_token_9', '2024-04-18 20:00:00');
-- password 123 or string
-- Chèn dữ liệu vào bảng water_bills
INSERT INTO water_bills (user_id, prev_volume, cur_volume, total_volume, price, total_volume_price, due_date, payment_date, created_at, created_by)
VALUES
    (1, 100, 120, 20, 1000, 20000, '2024-04-30', '2024-04-20', NOW() - INTERVAL '1 day', 13),
    (2, 80, 110, 30, 2000, 60000, '2024-05-01', '2024-04-21', NOW() - INTERVAL '2 day', 13),
    (3, 150, 180, 30, 2000, 60000, '2024-05-02', '2024-04-22', NOW() - INTERVAL '3 day', 2),
    (4, 70, 90, 20, 1000, 20000, '2024-05-03', '2024-04-23', NOW() - INTERVAL '4 day', 12),
    (5, 120, 150, 30, 2000, 60000, '2024-05-04', '2024-04-24', NOW() - INTERVAL '5 day', 12),
    (6, 50, 80, 30, 2000, 60000, '2024-05-05', '2024-04-25', NOW() - INTERVAL '6 day', 2),
    (7, 110, 140, 30, 2000, 60000, '2024-05-06', '2024-04-26', NOW() - INTERVAL '7 day', 13),
    (8, 90, 120, 30, 2000, 60000, '2024-05-07', '2024-04-27', NOW() - INTERVAL '8 day', 12),
    (9, 130, 160, 30, 2000, 60000, '2024-05-08', '2024-04-28', NOW() - INTERVAL '9 day', 1),
    (10, 100, 130, 30, 2000, 60000, '2024-05-09', '2024-04-29', NOW() - INTERVAL '10 day', 1);

INSERT INTO users (role, username, hashed_password, email, dob, code, expiry, refresh_token, last_login)
VALUES
    ('admin', 'tun admin', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'nddat1811@gmail.com', '1990-01-01', 'code1', '2025-01-01', 'refresh_token_1', '2024-04-18 12:00:00'),
    ('staff', 'tun staff', '$2b$12$G1m2LX8fhIB/y5CPI2J/U.qCki85RxcEMloTkxrHTM3HSgdZaRT6u', 'nddat18111@gmail.com', '1993-10-10', 'code10', '2025-10-10', 'refresh_token_10', '2024-04-18 21:00:00');
