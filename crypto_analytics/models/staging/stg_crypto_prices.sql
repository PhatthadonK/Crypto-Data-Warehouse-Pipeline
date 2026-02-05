with source as (
    select * from {{ source('raw_data', 'crypto_prices') }}
),

renamed as (
    select
        symbol,
        name,
        round(price_usd::numeric, 2) as price_usd,
        volume_24h,
        rank,
        captured_at
    from source
)

select * from renamed