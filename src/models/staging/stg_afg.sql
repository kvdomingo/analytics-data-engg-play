SELECT
    * EXCLUDE (
        school_id_giga,
        school_id_govt,
        school_name,
        latitude,
        longitude,
        education_level
    ),
    school_id_giga::VARCHAR(36) AS school_id_giga,
    school_id_govt::STRING AS school_id_govt,
    school_name::STRING AS school_name,
    latitude::DECIMAL(8, 5) AS latitude,
    longitude::DECIMAL(8, 5) AS longitude,
    education_level::STRING AS education_level
FROM {{ source('ae_de_play', 'raw_afg') }}
