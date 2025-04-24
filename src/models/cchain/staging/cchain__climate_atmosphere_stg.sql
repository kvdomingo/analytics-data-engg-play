SELECT
    uuid,
    adm4_pcode,
    date::DATE AS date,
    freq,
    tave::FLOAT AS tave,
    tmin::FLOAT AS tmin,
    tmax::FLOAT AS tmax,
    heat_index::FLOAT AS heat_index,
    pr::FLOAT AS pr,
    wind_speed::FLOAT AS wind_speed,
    rh::FLOAT AS rh,
    solar_rad::FLOAT AS solar_rad,
    uv_rad::FLOAT AS uv_rad
FROM {{ source('ae_de_play', 'cchain__climate_atmosphere_raw') }}
