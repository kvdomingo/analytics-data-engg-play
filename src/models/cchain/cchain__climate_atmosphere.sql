SELECT
    uuid AS id,
    adm4_pcode,
    date,
    freq AS frequency,
    tave AS temperature_ave,
    tmin AS temperature_min,
    tmax AS temperature_max,
    heat_index,
    pr AS precipitation,
    wind_speed,
    rh AS relative_humidity,
    solar_rad AS solar_radiance,
    uv_rad AS uv_radiance
FROM {{ ref('cchain__climate_atmosphere_stg') }}
