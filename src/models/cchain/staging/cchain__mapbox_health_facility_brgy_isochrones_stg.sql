SELECT
    uuid,
    adm4_pcode,
    date::DATE AS date,
    freq,
    brgy_healthcenter_pop_reached_5min::FLOAT AS brgy_healthcenter_pop_reached_5min,
    brgy_healthcenter_pop_reached_15min::FLOAT AS brgy_healthcenter_pop_reached_15min,
    brgy_healthcenter_pop_reached_30min::FLOAT AS brgy_healthcenter_pop_reached_30min,
    brgy_healthcenter_pop_reached_pct_5min::FLOAT
        AS brgy_healthcenter_pop_reached_pct_5min,
    brgy_healthcenter_pop_reached_pct_15min::FLOAT
        AS brgy_healthcenter_pop_reached_pct_15min,
    brgy_healthcenter_pop_reached_pct_30min::FLOAT
        AS brgy_healthcenter_pop_reached_pct_30min,
    hospital_pop_reached_5min::FLOAT AS hospital_pop_reached_5min,
    hospital_pop_reached_15min::FLOAT AS hospital_pop_reached_15min,
    hospital_pop_reached_30min::FLOAT AS hospital_pop_reached_30min,
    hospital_pop_reached_pct_5min::FLOAT AS hospital_pop_reached_pct_5min,
    hospital_pop_reached_pct_15min::FLOAT AS hospital_pop_reached_pct_15min,
    hospital_pop_reached_pct_30min::FLOAT AS hospital_pop_reached_pct_30min,
    rhu_pop_reached_5min::FLOAT AS rhu_pop_reached_5min,
    rhu_pop_reached_15min::FLOAT AS rhu_pop_reached_15min,
    rhu_pop_reached_30min::FLOAT AS rhu_pop_reached_30min,
    rhu_pop_reached_pct_5min::FLOAT AS rhu_pop_reached_pct_5min,
    rhu_pop_reached_pct_15min::FLOAT AS rhu_pop_reached_pct_15min,
    rhu_pop_reached_pct_30min::FLOAT AS rhu_pop_reached_pct_30min
FROM {{ source('ae_de_play', 'cchain__mapbox_health_facility_brgy_isochrones_raw') }}
