-- Federal Funds Rate table
CREATE TABLE IF NOT EXISTS federal_funds_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    rate DECIMAL(5,2) NOT NULL,
    rate_change DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_ffr_date ON federal_funds_rates(date DESC);
CREATE INDEX IF NOT EXISTS idx_ffr_rate ON federal_funds_rates(rate);

-- Analytics summary table
CREATE TABLE IF NOT EXISTS rate_analytics (
    id SERIAL PRIMARY KEY,
    calculation_date DATE NOT NULL,
    avg_30_day DECIMAL(5,2),
    avg_90_day DECIMAL(5,2),
    avg_365_day DECIMAL(5,2),
    volatility_30_day DECIMAL(8,4),
    min_rate_ytd DECIMAL(5,2),
    max_rate_ytd DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_analytics_date ON rate_analytics(calculation_date DESC);
