SELECT
    uuid,
    freq,
    date::DATE AS date,
    source_name,
    source_filename,
    adm3_pcode,
    disease_icd10_code,
    disease_common_name,
    case_total::UINTEGER AS case_total
FROM {{ source('ae_de_play', 'cchain__disease_pidsr_totals_raw') }}
