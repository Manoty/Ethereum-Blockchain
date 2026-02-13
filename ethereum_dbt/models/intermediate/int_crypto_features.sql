{{ config(materialized='view') }}

-- Intermediate crypto features: daily returns, moving averages, volatility
with base as (

    select *
    from {{ ref('stg_all_crypto') }}

),

returns as (

    select
        asset,
        date,
        close_price,
        volume,

        -- Daily return
        (close_price - lag(close_price) over (partition by asset order by date))
        / lag(close_price) over (partition by asset order by date) as daily_return

    from base

),

moving_averages as (

    select
        *,
        
        -- 7-day moving average of close price
        avg(close_price) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as ma_7,

        -- 30-day moving average of close price
        avg(close_price) over (
            partition by asset
            order by date
            rows between 29 preceding and current row
        ) as ma_30,

        -- 7-day rolling volatility (standard deviation of daily returns)
        stddev(daily_return) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as volatility_7

    from returns

)

select *
from moving_averages
order by asset, date
