USE stock_reporting;

DELIMITER $$

-- Report: price history for a symbol in a date range
CREATE PROCEDURE sp_price_history (
  IN p_symbol VARCHAR(16),
  IN p_start DATETIME,
  IN p_end DATETIME
)
BEGIN
  SELECT s.symbol, pt.price, pt.fetched_at, pt.source
  FROM price_ticks pt
  JOIN symbols s ON s.id = pt.symbol_id
  WHERE s.symbol = p_symbol
    AND pt.fetched_at BETWEEN p_start AND p_end
  ORDER BY pt.fetched_at ASC;
END$$

-- Report: latest prices (dashboard-ready)
CREATE PROCEDURE sp_latest_prices ()
BEGIN
  SELECT * FROM vw_latest_price ORDER BY symbol;
END$$

DELIMITER ;
