WITH
t1 AS (
    SELECT
        id AS product_id,
        retrieved_at,
        UNNEST(variants) AS variant
    FROM {{ ref('gpu_tracker__dynaquest_products_bronze') }}
),
t2 AS (
    SELECT
        variant.id::TEXT AS source_id,
        t1.product_id,
        'dynaquest.com' AS domain_tld,
        variant.title,
        variant.available AS is_available,
        variant.price::FLOAT AS price,
        variant.grams::FLOAT AS weight,
        t1.retrieved_at
    FROM t1
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['domain_tld', 'product_id', 'source_id']) }} AS id,
    *
FROM t2
