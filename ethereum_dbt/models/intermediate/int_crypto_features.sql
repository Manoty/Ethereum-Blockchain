{{ config(materialized='view') }}

with base as (

    select
        asset,
        date,
        close_price,
        volume
    from {{ ref('stg_all_crypto') }}

),

returns as (

    select
        asset,
        date,
        close_price,
        volume,
        -- Daily return with nullif to prevent divide-by-zero
        (close_price - lag(close_price)
            over (partition by asset order by date))
        / nullif(
            lag(close_price) over (partition by asset order by date),
            0
        ) as daily_return
    from base

),

moving_averages as (

    select
        *,
        -- 7-day moving average
        avg(close_price)
            over (
                partition by asset
                order by date
                rows between 6 preceding and current row
            ) as ma_7,

        -- 30-day moving average
        avg(close_price)
            over (
                partition by asset
                order by date
                rows between 29 preceding and current row
            ) as ma_30,

        -- 7-day rolling volatility (std dev of returns)
        stddev(daily_return)
            over (
                partition by asset
                order by date
                rows between 6 preceding and current row
            ) as volatility_7

    from returns

)

select *
from moving_averages
