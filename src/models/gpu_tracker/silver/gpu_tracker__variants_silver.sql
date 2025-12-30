SELECT * FROM {{ ref('gpu_tracker__dynaquest_variants_bronze') }}
UNION BY NAME
SELECT * FROM {{ ref('gpu_tracker__datablitz_variants_bronze') }}
UNION BY NAME
SELECT * FROM {{ ref('gpu_tracker__easypc_variants_bronze') }}
