{% set coins = [
    'bitcoin',
    'ethereum',
    'solana',
    'dogecoin',
    'cardano',
    'xrp'
] %}
-- Add the rest of your coins here gradually

{% for coin in coins %}

select
    '{{ coin }}' as asset,
    cast(Date as date) as date,
    cast(Open as double) as open_price,
    cast(High as double) as high_price,
    cast(Low as double) as low_price,
    cast(Close as double) as close_price,
    cast(Volume as double) as volume
from {{ ref(coin) }}

{% if not loop.last %} union all {% endif %}

{% endfor %}
