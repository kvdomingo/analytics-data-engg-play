SELECT
    uuid,
    freq,
    date::DATE AS date,
    source_name,
    source_filename,
    adm3_pcode,
    adm4_pcode,
    disease_icd10_code,
    disease_common_name,
    sex,
    age_group,
    case_total::INTEGER AS case_total,
    death_total::INTEGER AS death_total
FROM {{ source('ae_de_play', 'cchain__disease_lgu_disaggregated_totals_raw') }}
