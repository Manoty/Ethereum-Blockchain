-- models/intermediate/int_daily_asset_metrics.sql

with features as (
    select
        asset,
        date,
        cast(open_price as double) as open_price,
        cast(close_price as double) as close_price,
        cast(volume as double) as volume,
        
        -- daily return
        case
            when open_price is not null and cast(open_price as double) != 0
            then (cast(close_price as double) - cast(open_price as double)) / cast(open_price as double)
            else null
        end as daily_return
    from {{ ref('int_crypto_features') }}
),

metrics as (
    select
        asset,
        date,
        close_price,
        daily_return,
        -- rolling 7-day volatility example
        stddev_samp(daily_return) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as rolling_vol_7d,

        -- simple moving average 7-day
        avg(close_price) over (
            partition by asset
            order by date
            rows between 6 preceding and current row
        ) as sma_7d

    from features
)

select *
from metrics
