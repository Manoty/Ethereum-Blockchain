{{ config(materialized='view') }}

-- Safely get seed tables (won't crash if none exist yet)
{% set relations = [] %}
{% if execute %}
    {% set relations = dbt_utils.get_relations_by_pattern(
        schema_pattern=target.schema,
        table_pattern='%'
    ) %}
{% endif %}

{% set seed_tables = [] %}

{% for relation in relations %}
    {% if relation.type == 'table' and relation.identifier != 'stg_all_crypto' %}
        {% do seed_tables.append(relation) %}
    {% endif %}
{% endfor %}

-- If no tables, just return empty set (compiles safely)
{% if seed_tables | length == 0 %}
select
    null as asset,
    null::date as date,
    null::double as open_price,
    null::double as high_price,
    null::double as low_price,
    null::double as close_price,
    null::double as volume
where false
{% else %}

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

{% if not loop.last %}
union all
{% endif %}

{% endfor %}
{% endif %}
