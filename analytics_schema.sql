-- analytics_schema.sql
-- Database schema extensions for Analytics Dashboard

CREATE TABLE IF NOT EXISTS farm_yield (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    crop VARCHAR(128) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    yield DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS farm_revenue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS farm_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    target_yield DECIMAL(10,2),
    target_revenue DECIMAL(12,2),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
