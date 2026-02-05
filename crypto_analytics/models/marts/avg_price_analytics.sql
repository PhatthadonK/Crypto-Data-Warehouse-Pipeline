with staging as (
    -- CORRECT: Uses ref() to point to the staging model
    select * from {{ ref('stg_crypto_prices') }}
),

analytics as (
    select
        symbol,
        name,
        count(*) as data_points_collected,
        round(avg(price_usd), 2) as avg_price,
        round(max(price_usd), 2) as max_price,
        round(min(price_usd), 2) as min_price,
        round(max(price_usd) - min(price_usd), 2) as volatility,
        max(captured_at) as last_updated
    from staging
    group by symbol, name
)

select * from analytics
order by volatility desc