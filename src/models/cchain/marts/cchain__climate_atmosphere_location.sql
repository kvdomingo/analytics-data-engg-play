SELECT
    ca.id,
    ca.date,
    ca.temperature_ave,
    ca.temperature_min,
    ca.temperature_max,
    ca.heat_index,
    ca.precipitation,
    ca.wind_speed,
    ca.relative_humidity,
    ca.solar_radiance,
    ca.uv_radiance,
    l.adm1_en,
    l.adm1_pcode,
    l.adm2_en,
    l.adm2_pcode,
    l.adm3_en,
    l.adm3_pcode
FROM {{ ref('cchain__climate_atmosphere') }} AS ca
LEFT JOIN {{ ref('cchain__location') }} AS l USING (adm4_pcode)
ORDER BY ca.date, adm4_pcode
