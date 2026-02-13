-- models/staging/stg_all_crypto.sql
-- Staging model: combines all crypto CSVs into one table

with all_data as (

    select 'aave' as asset, date, open as open_price, high, low, close as close_price, volume
    from read_csv_auto('seeds/aave.csv')

    union all
    select 'algorand', date, open, high, low, close, volume
    from read_csv_auto('seeds/algorand.csv')

    union all
    select 'aptos', date, open, high, low, close, volume
    from read_csv_auto('seeds/aptos.csv')

    union all
    select 'arbitrum', date, open, high, low, close, volume
    from read_csv_auto('seeds/arbitrum.csv')

    union all
    select 'avalanche', date, open, high, low, close, volume
    from read_csv_auto('seeds/avalanche.csv')

    union all
    select 'axie_infinity', date, open, high, low, close, volume
    from read_csv_auto('seeds/axie_infinity.csv')

    union all
    select 'binance_coin', date, open, high, low, close, volume
    from read_csv_auto('seeds/binance_coin.csv')

    union all
    select 'bitcoin', date, open, high, low, close, volume
    from read_csv_auto('seeds/bitcoin.csv')

    union all
    select 'bitcoin_cash', date, open, high, low, close, volume
    from read_csv_auto('seeds/bitcoin_cash.csv')

    union all
    select 'cardano', date, open, high, low, close, volume
    from read_csv_auto('seeds/cardano.csv')

    union all
    select 'chainlink', date, open, high, low, close, volume
    from read_csv_auto('seeds/chainlink.csv')

    union all
    select 'cosmos', date, open, high, low, close, volume
    from read_csv_auto('seeds/cosmos.csv')

    union all
    select 'decentraland', date, open, high, low, close, volume
    from read_csv_auto('seeds/decentraland.csv')

    union all
    select 'dogecoin', date, open, high, low, close, volume
    from read_csv_auto('seeds/dogecoin.csv')

    union all
    select 'eos', date, open, high, low, close, volume
    from read_csv_auto('seeds/eos.csv')

    union all
    select 'ethereum', date, open, high, low, close, volume
    from read_csv_auto('seeds/ethereum.csv')

    union all
    select 'fantom', date, open, high, low, close, volume
    from read_csv_auto('seeds/fantom.csv')

    union all
    select 'filecoin', date, open, high, low, close, volume
    from read_csv_auto('seeds/filecoin.csv')

    union all
    select 'flow', date, open, high, low, close, volume
    from read_csv_auto('seeds/flow.csv')

    union all
    select 'hedera', date, open, high, low, close, volume
    from read_csv_auto('seeds/hedera.csv')

    union all
    select 'immutable', date, open, high, low, close, volume
    from read_csv_auto('seeds/immutable.csv')

    union all
    select 'injective', date, open, high, low, close, volume
    from read_csv_auto('seeds/injective.csv')

    union all
    select 'internet_computer', date, open, high, low, close, volume
    from read_csv_auto('seeds/internet_computer.csv')

    union all
    select 'kaspa', date, open, high, low, close, volume
    from read_csv_auto('seeds/kaspa.csv')

    union all
    select 'lido', date, open, high, low, close, volume
    from read_csv_auto('seeds/lido.csv')

    union all
    select 'litecoin', date, open, high, low, close, volume
    from read_csv_auto('seeds/litecoin.csv')

    union all
    select 'maker', date, open, high, low, close, volume
    from read_csv_auto('seeds/maker.csv')

    union all
    select 'near', date, open, high, low, close, volume
    from read_csv_auto('seeds/near.csv')

    union all
    select 'optimism', date, open, high, low, close, volume
    from read_csv_auto('seeds/optimism.csv')

    union all
    select 'pepe', date, open, high, low, close, volume
    from read_csv_auto('seeds/pepe.csv')

    union all
    select 'polkadot', date, open, high, low, close, volume
    from read_csv_auto('seeds/polkadot.csv')

    union all
    select 'polygon', date, open, high, low, close, volume
    from read_csv_auto('seeds/polygon.csv')

    union all
    select 'render', date, open, high, low, close, volume
    from read_csv_auto('seeds/render.csv')

    union all
    select 'sandbox', date, open, high, low, close, volume
    from read_csv_auto('seeds/sandbox.csv')

    union all
    select 'shiba_inu', date, open, high, low, close, volume
    from read_csv_auto('seeds/shiba_inu.csv')

    union all
    select 'solana', date, open, high, low, close, volume
    from read_csv_auto('seeds/solana.csv')

    union all
    select 'stacks', date, open, high, low, close, volume
    from read_csv_auto('seeds/stacks.csv')

    union all
    select 'stellar', date, open, high, low, close, volume
    from read_csv_auto('seeds/stellar.csv')

    union all
    select 'sui', date, open, high, low, close, volume
    from read_csv_auto('seeds/sui.csv')

    union all
    select 'tether', date, open, high, low, close, volume
    from read_csv_auto('seeds/tether.csv')

    union all
    select 'tezos', date, open, high, low, close, volume
    from read_csv_auto('seeds/tezos.csv')

    union all
    select 'theta', date, open, high, low, close, volume
    from read_csv_auto('seeds/theta.csv')

    union all
    select 'the_graph', date, open, high, low, close, volume
    from read_csv_auto('seeds/the_graph.csv')

    union all
    select 'toncoin', date, open, high, low, close, volume
    from read_csv_auto('seeds/toncoin.csv')

    union all
    select 'tron', date, open, high, low, close, volume
    from read_csv_auto('seeds/tron.csv')

    union all
    select 'uniswap', date, open, high, low, close, volume
    from read_csv_auto('seeds/uniswap.csv')

    union all
    select 'usd_coin', date, open, high, low, close, volume
    from read_csv_auto('seeds/usd_coin.csv')

    union all
    select 'vechain', date, open, high, low, close, volume
    from read_csv_auto('seeds/vechain.csv')

    union all
    select 'xrp', date, open, high, low, close, volume
    from read_csv_auto('seeds/xrp.csv')

)

select *
from all_data
