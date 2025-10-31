WITH t1 AS (
    SELECT
        id AS product_id,
        retrieved_at,
        UNNEST(variants.edges).node AS variant
    FROM {{ ref('gpu_tracker__datablitz_products_bronze') }}
),
t2 AS (
    SELECT
        str_split(variant.id, '/')[-1]::TEXT AS source_id,
        product_id,
        'datablitz.com.ph' AS domain_tld,
        variant.title,
        variant.availableForSale AS is_available,
        variant.price.amount::FLOAT AS price,
        variant.weight::FLOAT * 1000 AS weight,
        retrieved_at
    FROM t1
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['domain_tld', 'product_id', 'source_id']) }} AS id,
    *
FROM t2
