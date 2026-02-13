{{ config(materialized='view') }}

with all_crypto as (

    select
        'aave' as asset,
        cast(date as date) as date,
        cast(open as double) as open_price,
        cast(high as double) as high,
        cast(low as double) as low,
        cast(close as double) as close_price,
        cast(volume as double) as volume
    from {{ ref('aave') }}

    union all

    select
        'algorand',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('algorand') }}

    union all

    select
        'aptos',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('aptos') }}

    union all

    select
        'arbitrum',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('arbitrum') }}

    union all

    select
        'avalanche',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('avalanche') }}

    union all

    select
        'axie_infinity',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('axie_infinity') }}

    union all

    select
        'binance_coin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('binance_coin') }}

    union all

    select
        'bitcoin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('bitcoin') }}

    union all

    select
        'bitcoin_cash',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('bitcoin_cash') }}

    union all

    select
        'cardano',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('cardano') }}

    union all

    select
        'chainlink',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('chainlink') }}

    union all

    select
        'cosmos',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('cosmos') }}

    union all

    select
        'decentraland',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('decentraland') }}

    union all

    select
        'dogecoin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('dogecoin') }}

    union all

    select
        'eos',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('eos') }}

    union all

    select
        'ethereum',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('ethereum') }}

    union all

    select
        'fantom',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('fantom') }}

    union all

    select
        'filecoin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('filecoin') }}

    union all

    select
        'flow',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('flow') }}

    union all

    select
        'hedera',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('hedera') }}

    union all

    select
        'immutable',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('immutable') }}

    union all

    select
        'injective',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('injective') }}

    union all

    select
        'internet_computer',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('internet_computer') }}

    union all

    select
        'kaspa',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('kaspa') }}

    union all

    select
        'lido',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('lido') }}

    union all

    select
        'litecoin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('litecoin') }}

    union all

    select
        'maker',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('maker') }}

    union all

    select
        'near',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('near') }}

    union all

    select
        'optimism',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('optimism') }}

    union all

    select
        'pepe',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('pepe') }}

    union all

    select
        'polkadot',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('polkadot') }}

    union all

    select
        'polygon',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('polygon') }}

    union all

    select
        'render',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('render') }}

    union all

    select
        'sandbox',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('sandbox') }}

    union all

    select
        'shiba_inu',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('shiba_inu') }}

    union all

    select
        'solana',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('solana') }}

    union all

    select
        'stacks',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('stacks') }}

    union all

    select
        'stellar',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('stellar') }}

    union all

    select
        'sui',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('sui') }}

    union all

    select
        'tether',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('tether') }}

    union all

    select
        'tezos',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('tezos') }}

    union all

    select
        'theta',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('theta') }}

    union all

    select
        'the_graph',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('the_graph') }}

    union all

    select
        'toncoin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('toncoin') }}

    union all

    select
        'tron',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('tron') }}

    union all

    select
        'uniswap',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('uniswap') }}

    union all

    select
        'usd_coin',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('usd_coin') }}

    union all

    select
        'vechain',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('vechain') }}

    union all

    select
        'xrp',
        cast(date as date),
        cast(open as double),
        cast(high as double),
        cast(low as double),
        cast(close as double),
        cast(volume as double)
    from {{ ref('xrp') }}

)

select *
from all_crypto
