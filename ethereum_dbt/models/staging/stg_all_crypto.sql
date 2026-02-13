{{ config(materialized='view') }}

{% set crypto_assets = [
    'aave','algorand','aptos','arbitrum','avalanche','axie_infinity','binance_coin',
    'bitcoin','bitcoin_cash','cardano','chainlink','cosmos','decentraland','dogecoin',
    'eos','ethereum','fantom','filecoin','flow','hedera','immutable','injective',
    'internet_computer','kaspa','lido','litecoin','maker','near','optimism','pepe',
    'polkadot','polygon','render','sandbox','shiba_inu','solana','stacks','stellar',
    'sui','tether','tezos','theta','the_graph','toncoin','tron','uniswap','usd_coin','vechain','xrp'
] %}

{% set union_queries = [] %}

{% for asset in crypto_assets %}

    {% set table_ref = ref(asset) %}

    {% set query %}
    select
        '{{ asset }}' as asset,
        cast(Date as date) as date,
        try_cast(Open as double) as open_price,
        try_cast(High as double) as high_price,
        try_cast(Low as double) as low_price,
        try_cast(Close as double) as close_price,
        try_cast(Volume as double) as volume
    from {{ table_ref }}
    where try_cast(Close as double) is not null
    {% endset %}

    {% do union_queries.append(query) %}

{% endfor %}

{{ union_queries | join('\nunion all\n') }}
