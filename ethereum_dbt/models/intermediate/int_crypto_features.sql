-- models/intermediate/int_crypto_features.sql

with base as (
    select-- models/intermediate/int_crypto_features.sql

with base as (
    select
        asset,
        date,
        cast(open_price as double) as open_price,
        cast(close_price as double) as close_price,
        cast(high as double) as high,
        cast(low as double) as low,
        cast(volume as double) as volume,

        -- daily return
        case
            when open_price is not null and cast(open_price as double) != 0
            then (cast(close_price as double) - cast(open_price as double)) / cast(open_price as double)
            else null
        end as daily_return,

        -- log return
        case
            when open_price is not null and cast(open_price as double) > 0
                 and close_price is not null and cast(close_price as double) > 0
            then ln(cast(close_price as double) / cast(open_price as double))
            else null
        end as log_return

    from {{ ref('stg_all_crypto') }}
)

select *
from base

        asset,
        date,
        cast(open_price as double) as open_price,
        cast(close_price as double) as close_price,
        cast(high as double) as high,
        cast(low as double) as low,
        cast(volume as double) as volume,

        -- daily return
        case
            when open_price is not null and cast(open_price as double) != 0
            then (cast(close_price as double) - cast(open_price as double)) / cast(open_price as double)
            else null
        end as daily_return,

        -- log return
        case
            when open_price is not null and cast(open_price as double) > 0
                 and close_price is not null and cast(close_price as double) > 0
            then ln(cast(close_price as double) / cast(open_price as double))
            else null
        end as log_return

    from {{ ref('stg_all_crypto') }}
)

select *
from base
