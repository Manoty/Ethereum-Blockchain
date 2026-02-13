with base as (

    select
        asset,
        date,
        open_price,
        close_price,
        high_price,
        low_price,
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

)

select *
from base
