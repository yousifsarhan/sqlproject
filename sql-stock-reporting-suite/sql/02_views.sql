USE stock_reporting;

-- Latest price per symbol
CREATE OR REPLACE VIEW vw_latest_price AS
SELECT s.symbol, s.name, pt.price, pt.fetched_at
FROM symbols s
JOIN price_ticks pt ON pt.symbol_id = s.id
JOIN (
  SELECT symbol_id, MAX(fetched_at) AS max_time
  FROM price_ticks
  GROUP BY symbol_id
) x ON x.symbol_id = pt.symbol_id AND x.max_time = pt.fetched_at;

-- Minute-level aggregation (simple)
CREATE OR REPLACE VIEW vw_minute_prices AS
SELECT
  s.symbol,
  DATE_FORMAT(pt.fetched_at, '%Y-%m-%d %H:%i:00') AS minute_bucket,
  AVG(pt.price) AS avg_price,
  MIN(pt.price) AS min_price,
  MAX(pt.price) AS max_price,
  COUNT(*) AS samples
FROM price_ticks pt
JOIN symbols s ON s.id = pt.symbol_id
GROUP BY s.symbol, DATE_FORMAT(pt.fetched_at, '%Y-%m-%d %H:%i:00');
