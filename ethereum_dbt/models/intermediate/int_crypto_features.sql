with base as (

    select
        asset,
        date,
        open_price,
        close_price,
        high,
        low,
        volume,

        case
            when open_price > 0
            then (close_price - open_price) / open_price
            else null
        end as daily_return,

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

)

select *
from base
