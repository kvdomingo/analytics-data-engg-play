SELECT * FROM {{ ref('gpu_tracker__dynaquest_bronze') }}
UNION BY NAME
SELECT * FROM {{ ref('gpu_tracker__datablitz_bronze') }}
