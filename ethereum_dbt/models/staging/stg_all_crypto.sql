{{ config(materialized='view') }}

-- Hardcode schema to main
{% set relations = dbt_utils.get_relations_by_pattern(
    schema_pattern='main',
    table_pattern='%'
) %}

-- Filter out THIS model + only include tables that exist (seeds)
{% set seed_tables = [] %}
{% for relation in relations %}
    {% if relation.type == 'table' and relation.identifier != 'stg_all_crypto' %}
        {% do seed_tables.append(relation) %}
    {% endif %}
{% endfor %}

-- Fail fast if nothing found
{% if seed_tables | length == 0 %}
    {{ exceptions.raise_compiler_error("No seed tables found in main schema. Run dbt seed first.") }}
{% endif %}

-- Union all crypto tables
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
