SELECT * EXCLUDE (variants) FROM {{ ref('gpu_tracker__dynaquest_products_bronze') }}
UNION BY NAME
SELECT * EXCLUDE (variants) FROM {{ ref('gpu_tracker__datablitz_products_bronze') }}
UNION BY NAME
SELECT * EXCLUDE (variants) FROM {{ ref('gpu_tracker__easypc_products_bronze') }}
