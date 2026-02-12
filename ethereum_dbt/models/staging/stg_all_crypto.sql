{% set relations = dbt_utils.get_relations_by_pattern(
    schema=target.schema,
    pattern='%'
) %}

{% set seed_tables = [] %}

{% for relation in relations %}
    {% if relation.identifier not in ['stg_all_crypto'] %}
        {% do seed_tables.append(relation) %}
    {% endif %}
{% endfor %}

{% for table in seed_tables %}

select
    '{{ table.identifier }}' as asset,
    cast(Date as date) as date,
    cast(Open as double) as open_price,
    cast(High as double) as high_price,
    cast(Low as double) as low_price,
    cast(Close as double) as close_price,
    cast(Volume as double) as volume
from {{ table }}

{% if not loop.last %} union all {% endif %}

{% endfor %}
