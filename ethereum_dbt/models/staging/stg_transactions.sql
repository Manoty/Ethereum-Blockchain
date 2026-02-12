with raw as (
    select *
    from {{ source('ethereum', 'transactions') }}
)

select
    hash as tx_hash,
    from_address,
    to_address,
    value as value_eth,
    block_timestamp
from raw
