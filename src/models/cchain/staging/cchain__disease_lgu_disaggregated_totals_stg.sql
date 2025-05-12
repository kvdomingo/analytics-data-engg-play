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
    case_total::INTEGER AS case_total,
    CASE
        WHEN age_group = '5-10'
            THEN '5-9'
        ELSE age_group
    END AS age_group,
    COALESCE(death_total::INTEGER, 0) AS death_total
FROM {{ source('ae_de_play', 'cchain__disease_lgu_disaggregated_totals_raw') }}
