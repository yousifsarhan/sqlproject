CREATE DATABASE IF NOT EXISTS stock_reporting;
USE stock_reporting;

CREATE TABLE IF NOT EXISTS symbols (
  id INT AUTO_INCREMENT PRIMARY KEY,
  symbol VARCHAR(16) NOT NULL UNIQUE,
  name VARCHAR(128) NULL
);
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'app123';
GRANT ALL PRIVILEGES ON stock_reporting.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS price_ticks (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  symbol_id INT NOT NULL,
  price DECIMAL(18,6) NOT NULL,
  fetched_at DATETIME NOT NULL,
  source VARCHAR(32) NOT NULL,
  INDEX idx_symbol_time (symbol_id, fetched_at),
  CONSTRAINT fk_symbol FOREIGN KEY (symbol_id) REFERENCES symbols(id)
);

INSERT IGNORE INTO symbols(symbol, name) VALUES
('SPY','S&P 500 ETF'),
('NVDA','NVIDIA'),
('TSLA','Tesla');

