SELECT
    * EXCLUDE (uuid),
    uuid AS id
FROM {{ ref('cchain__mapbox_health_facility_brgy_isochrones_stg') }}
