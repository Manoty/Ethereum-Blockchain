-- models/intermediate/int_crypto_features.sql

with base as (

    select
        asset,
        date,
        open_price,
        close_price,
        high,
        low,
        volume,

        -- daily return
        case
            when open_price > 0
            then (close_price - open_price) / open_price
            else null
        end as daily_return,

        -- log return
        case
            when open_price > 0
             and close_price > 0
            then ln(close_price / open_price)
            else null
        end as log_return

    from {{ ref('stg_all_crypto') }}

    -- 🔥 CLEAN BAD ROWS
    where open_price > 0
      and close_price > 0
      and volume > 0

),

-- ------------------------------
-- 1️⃣ Add cumulative return
-- ------------------------------
cum as (
    select
        *,
        -- cumulative return: close price divided by first close price in the dataset
        close_price / first_value(close_price) over (partition by asset order by date) - 1 as cum_return
    from base
),

-- ------------------------------
-- 2️⃣ Add rolling metrics
-- ------------------------------
rolling as (
    select
        *,
        -- 7-day rolling volatility
        stddev_samp(daily_return) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as daily_return_7d_vol,

        -- 7-day rolling Sharpe ratio (assuming risk-free rate ~0)
        case
            when stddev_samp(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                 ) > 0
            then
                avg(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                ) / stddev_samp(daily_return) over (
                    partition by asset
                    order by date
                    rows between 6 preceding and current row
                )
            else null
        end as daily_return_7d_sharpe

    from cum
)

select *
from rolling
order by asset, date
