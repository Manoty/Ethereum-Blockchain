select
    asset,
    date,
    close_price,
    daily_return,
    volume
from {{ ref('int_daily_asset_metrics') }}
