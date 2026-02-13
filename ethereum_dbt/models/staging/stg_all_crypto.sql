{{ config(materialized='view') }}

{% set seed_tables = [
    'aave',
    'algorand',
    'aptos',
    'arbitrum',
    'avalanche',
    'axie_infinity',
    'binance_coin',
    'bitcoin',
    'bitcoin_cash',
    'cardano',
    'chainlink',
    'cosmos',
    'decentraland',
    'dogecoin',
    'eos',
    'ethereum',
    'fantom',
    'filecoin',
    'flow',
    'hedera',
    'immutable',
    'injective',
    'internet_computer',
    'kaspa',
    'lido',
    'litecoin',
    'maker',
    'near',
    'optimism',
    'pepe',
    'polkadot',
    'polygon',
    'render',
    'sandbox',
    'shiba_inu',
    'solana',
    'stacks',
    'stellar',
    'sui',
    'tether',
    'tezos',
    'theta',
    'the_graph',
    'toncoin',
    'tron',
    'uniswap',
    'usd_coin',
    'vechain',
    'xrp'
] %}

{% for table_name in seed_tables %}

select
    '{{ table_name }}' as asset,
    cast(Date as date) as date,
    cast(Open as double) as open_price,
    cast(High as double) as high_price,
    cast(Low as double) as low_price,
    cast(Close as double) as close_price,
    cast(Volume as double) as volume
from {{ ref(table_name) }}

{% if not loop.last %}
union all
{% endif %}

{% endfor %}
