with source as (

    select *, 'aave' as asset from {{ ref('aave') }}
    union all
    select *, 'algorand' as asset from {{ ref('algorand') }}
    union all
    select *, 'aptos' as asset from {{ ref('aptos') }}
    union all
    select *, 'arbitrum' as asset from {{ ref('arbitrum') }}
    union all
    select *, 'avalanche' as asset from {{ ref('avalanche') }}
    union all
    select *, 'axie_infinity' as asset from {{ ref('axie_infinity') }}
    union all
    select *, 'binance_coin' as asset from {{ ref('binance_coin') }}
    union all
    select *, 'bitcoin' as asset from {{ ref('bitcoin') }}
    union all
    select *, 'bitcoin_cash' as asset from {{ ref('bitcoin_cash') }}
    union all
    select *, 'cardano' as asset from {{ ref('cardano') }}
    union all
    select *, 'chainlink' as asset from {{ ref('chainlink') }}
    union all
    select *, 'cosmos' as asset from {{ ref('cosmos') }}
    union all
    select *, 'decentraland' as asset from {{ ref('decentraland') }}
    union all
    select *, 'dogecoin' as asset from {{ ref('dogecoin') }}
    union all
    select *, 'eos' as asset from {{ ref('eos') }}
    union all
    select *, 'ethereum' as asset from {{ ref('ethereum') }}
    union all
    select *, 'fantom' as asset from {{ ref('fantom') }}
    union all
    select *, 'filecoin' as asset from {{ ref('filecoin') }}
    union all
    select *, 'flow' as asset from {{ ref('flow') }}
    union all
    select *, 'hedera' as asset from {{ ref('hedera') }}
    union all
    select *, 'immutable' as asset from {{ ref('immutable') }}
    union all
    select *, 'injective' as asset from {{ ref('injective') }}
    union all
    select *, 'internet_computer' as asset from {{ ref('internet_computer') }}
    union all
    select *, 'kaspa' as asset from {{ ref('kaspa') }}
    union all
    select *, 'lido' as asset from {{ ref('lido') }}
    union all
    select *, 'litecoin' as asset from {{ ref('litecoin') }}
    union all
    select *, 'maker' as asset from {{ ref('maker') }}
    union all
    select *, 'near' as asset from {{ ref('near') }}
    union all
    select *, 'optimism' as asset from {{ ref('optimism') }}
    union all
    select *, 'pepe' as asset from {{ ref('pepe') }}
    union all
    select *, 'polkadot' as asset from {{ ref('polkadot') }}
    union all
    select *, 'polygon' as asset from {{ ref('polygon') }}
    union all
    select *, 'render' as asset from {{ ref('render') }}
    union all
    select *, 'sandbox' as asset from {{ ref('sandbox') }}
    union all
    select *, 'shiba_inu' as asset from {{ ref('shiba_inu') }}
    union all
    select *, 'solana' as asset from {{ ref('solana') }}
    union all
    select *, 'stacks' as asset from {{ ref('stacks') }}
    union all
    select *, 'stellar' as asset from {{ ref('stellar') }}
    union all
    select *, 'sui' as asset from {{ ref('sui') }}
    union all
    select *, 'tether' as asset from {{ ref('tether') }}
    union all
    select *, 'tezos' as asset from {{ ref('tezos') }}
    union all
    select *, 'the_graph' as asset from {{ ref('the_graph') }}
    union all
    select *, 'theta' as asset from {{ ref('theta') }}
    union all
    select *, 'toncoin' as asset from {{ ref('toncoin') }}
    union all
    select *, 'tron' as asset from {{ ref('tron') }}
    union all
    select *, 'uniswap' as asset from {{ ref('uniswap') }}
    union all
    select *, 'usd_coin' as asset from {{ ref('usd_coin') }}
    union all
    select *, 'vechain' as asset from {{ ref('vechain') }}
    union all
    select *, 'xrp' as asset from {{ ref('xrp') }}

),

cleaned as (

    select
        asset,
        date,

        try_cast(open as double) as open_price,
        try_cast(high as double) as high,
        try_cast(low as double) as low,
        try_cast(close as double) as close_price,
        try_cast(volume as double) as volume

    from source

)

select *
from cleaned
where open_price is not null
