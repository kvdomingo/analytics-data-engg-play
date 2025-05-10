SELECT
    dpt.id,
    dpt.date,
    dpt.disease_icd10_code,
    dpt.disease_common_name,
    dpt.case_total,
    l.adm1_en,
    l.adm1_pcode,
    l.adm2_en,
    l.adm2_pcode,
    l.adm3_en,
    l.adm3_pcode
FROM {{ ref('cchain__disease_pidsr_totals') }} AS dpt
LEFT JOIN {{ ref('cchain__location') }} AS l USING (adm3_pcode)
ORDER BY dpt.date, dpt.disease_icd10_code, adm3_pcode
