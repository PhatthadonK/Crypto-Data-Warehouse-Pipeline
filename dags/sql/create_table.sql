CREATE TABLE IF NOT EXISTS crypto_prices (
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(50),
    price_usd NUMERIC(18, 8),
    volume_24h NUMERIC(18, 2),
    rank INT,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);