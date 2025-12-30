WITH t1 AS (
    SELECT
        UNNEST(node),
        retrieved_at
    FROM {{ source('ae_de_play', 'gpu_tracker__datablitz_raw') }}
),
t2 AS (
    SELECT
        str_split(id, '/')[-1] AS source_id,
        'datablitz.com.ph' AS domain_tld,
        title,
        description,
        'https://ecommerce.datablitz.com.ph/collections/pc-mac/products/' || handle AS product_url,
        createdAt::TIMESTAMPTZ AS source_created_at,
        updatedAt::TIMESTAMPTZ AS source_updated_at,
        retrieved_at,
        vendor AS brand,
        images.edges[1].node.url AS image_url,
        list_min(
            list_transform(variants.edges, v -> v.node.price.amount::FLOAT)
        ) AS price_min,
        list_max(
            list_transform(variants.edges, v -> v.node.price.amount::FLOAT)
        ) AS price_max,
        variants
    FROM t1
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['domain_tld', 'source_id']) }} AS id,
    *
FROM t2
