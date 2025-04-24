SELECT
    adm1_en,
    adm1_pcode,
    adm2_en,
    adm2_pcode,
    adm3_en,
    adm3_pcode,
    adm4_en,
    adm4_pcode,
    brgy_total_area::FLOAT AS brgy_total_area
FROM {{ source('ae_de_play', 'cchain__location_raw') }}
