WITH t1 AS (
    SELECT
        id::TEXT AS source_id,
        'dynaquest.com' AS domain_tld,
        title,
        body_html AS description,
        'https://dynaquestpc.com/collections/graphics-card/products/' || handle AS product_url,
        created_at::TIMESTAMPTZ AS source_created_at,
        updated_at::TIMESTAMPTZ AS source_updated_at,
        retrieved_at,
        vendor AS brand,
        images[1].src AS image_url,
        list_min(
            list_transform(variants, v -> v.price::FLOAT)
        ) AS price_min,
        list_max(
            list_transform(variants, v -> v.price::FLOAT)
        ) AS price_max
    FROM {{ source('ae_de_play', 'gpu_tracker__dynaquest_raw') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['domain_tld', 'source_id']) }} AS id,
    *
FROM t1
