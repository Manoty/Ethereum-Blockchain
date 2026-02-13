{{ config(materialized='view') }}

-- Get all seed tables in the target schema
{% set relations = dbt_utils.get_relations_by_pattern(
    schema_pattern=target.schema,
    table_pattern='%'
) %}

-- Filter out THIS model itself only
{% set seed_tables = [] %}
{% for relation in relations %}
    {% if relation.identifier != 'stg_all_crypto' %}
        {% do seed_tables.append(relation) %}
    {% endif %}
{% endfor %}

-- Fail fast if no seeds found
{% if seed_tables | length == 0 %}
    {{ exceptions.raise_compiler_error("No seed tables found in schema. Run `dbt seed` first.") }}
{% endif %}

-- Union all seed tables dynamically
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
