SELECT
    id::TEXT AS id,
    title,
    handle,
    body_html,
    published_at::TIMESTAMPTZ AS published_at,
    created_at::TIMESTAMPTZ AS created_at,
    updated_at::TIMESTAMPTZ AS updated_at,
    vendor,
    variants,
    images,
    options,
    retrieved_at
FROM {{ source('ae_de_play', 'gpu_tracker__dynaquest_raw') }}
