-- models/intermediate/int_crypto_features.sql
-- Intermediate features: daily return, log return, simple transformations

with base as (

    select
        asset,
        date,
        open_price,
        close_price,
        high,
        low,
        volume,
        -- daily return: (close - open) / open
        case 
            when open_price is not null and open_price != 0 then (close_price - open_price) / open_price
            else null
        end as daily_return,
        -- log return: ln(close / open)
        case 
            when open_price is not null and open_price > 0 and close_price is not null and close_price > 0
            then ln(close_price / open_price)
            else null
        end as log_return

    from {{ ref('stg_all_crypto') }}

)

select *
from base
