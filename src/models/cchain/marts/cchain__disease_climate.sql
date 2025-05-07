WITH disease_agg AS (
    SELECT
        date,
        disease_icd10_code,
        FIRST(id) AS disease_id,
        FIRST(disease_common_name) AS disease_common_name,
        SUM(case_total) AS case_total,
        FIRST(adm1_en) AS adm1_en,
        FIRST(adm1_pcode) AS adm1_pcode,
        FIRST(adm2_en) AS adm2_en,
        FIRST(adm2_pcode) AS adm2_pcode,
        FIRST(adm3_en) AS adm3_en,
        FIRST(adm3_pcode) AS adm3_pcode
    FROM {{ ref('cchain__disease_pidsr_location') }}
    GROUP BY date, disease_icd10_code
),

climate_agg AS (
    SELECT
        date,
        FIRST(id) AS climate_id,
        AVG(temperature_ave) AS temperature_ave,
        MIN(temperature_min) AS temperature_min,
        MAX(temperature_max) AS temperature_max,
        AVG(heat_index) AS heat_index,
        AVG(precipitation) AS precipitation,
        AVG(wind_speed) AS wind_speed,
        AVG(relative_humidity) AS relative_humidity,
        AVG(solar_radiance) AS solar_radiance,
        AVG(uv_radiance) AS uv_radiance,
        FIRST(adm1_en) AS adm1_en,
        FIRST(adm1_pcode) AS adm1_pcode,
        FIRST(adm2_en) AS adm2_en,
        FIRST(adm2_pcode) AS adm2_pcode,
        FIRST(adm3_en) AS adm3_en,
        FIRST(adm3_pcode) AS adm3_pcode
    FROM {{ ref('cchain__climate_atmosphere_location') }}
    GROUP BY date, adm3_pcode
)

SELECT
    d.disease_id,
    c.climate_id,
    date,
    d.disease_icd10_code,
    d.disease_common_name,
    d.case_total,
    c.temperature_ave,
    c.temperature_min,
    c.temperature_max,
    c.heat_index,
    c.precipitation,
    c.wind_speed,
    c.relative_humidity,
    c.solar_radiance,
    c.uv_radiance,
    d.adm1_en,
    d.adm1_pcode,
    d.adm2_en,
    d.adm2_pcode,
    d.adm3_en,
    d.adm3_pcode
FROM disease_agg AS d
LEFT JOIN climate_agg AS c ON d.date = c.date AND d.adm3_pcode = c.adm3_pcode
ORDER BY date, d.disease_icd10_code, d.adm3_pcode
