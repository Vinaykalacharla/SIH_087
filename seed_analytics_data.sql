-- seed_analytics_data.sql
-- Sample data for analytics tables for user_id = 1

INSERT INTO farm_yield (user_id, crop, year, month, yield) VALUES
(1, 'Wheat', 2023, 1, 10.5),
(1, 'Wheat', 2023, 2, 12.0),
(1, 'Corn', 2023, 1, 8.0),
(1, 'Corn', 2023, 2, 9.5);

INSERT INTO farm_revenue (user_id, year, month, revenue) VALUES
(1, 2023, 1, 15000.00),
(1, 2023, 2, 18000.00);

INSERT INTO farm_goals (user_id, year, month, target_yield, target_revenue) VALUES
(1, 2023, 1, 11.0, 16000.00),
(1, 2023, 2, 13.0, 19000.00);
