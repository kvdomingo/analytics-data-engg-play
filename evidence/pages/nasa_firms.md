# NASA FIRMS Open Viz

```sql viirs
SELECT *,
       bright_ti4 - 273.15 AS ti4_c,
       bright_ti5 - 273.15 AS ti5_c
FROM viirs
WHERE country_id = 'PHL'
```

<PointMap
  data={viirs}
  lat=lat
  long=lng
  value=ti4_c
  colorPalette={['green', 'orange', 'red']}
/>
