SELECT
    uuid,
    adm4_pcode,
    date::DATE AS date,
    freq,
    tave::FLOAT AS tave,
    tmin::FLOAT AS tmin,
    tmax::FLOAT AS tmax,
    heat_index::FLOAT AS heat_index,
    wind_speed::FLOAT AS wind_speed,
    rh::FLOAT AS rh,
    solar_rad::FLOAT AS solar_rad,
    uv_rad::FLOAT AS uv_rad,
    COALESCE(pr::FLOAT, 0.0) AS pr
FROM {{ source('ae_de_play', 'cchain__climate_atmosphere_raw') }}
