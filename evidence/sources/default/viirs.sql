INSTALL spatial;
LOAD spatial;

SELECT
    * EXCLUDE(geometry),
    ST_AsText(geometry) AS geometry,
    ST_X(geometry) AS lat,
    ST_Y(geometry) AS lng
FROM ae_de_play.nasa_firms__viirs
