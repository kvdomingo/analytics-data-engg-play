# Project CCHAIN Open Viz

## Visualizing precipitation and dengue cases peaks in Dagupan

```sql disease_climate
WITH smoothed AS (SELECT
                      DATE_TRUNC('month', "date") AS "month",
                      EXTRACT(MONTH FROM "date")  AS month_number,
                      EXTRACT(YEAR FROM "date")   AS "year",
                      AVG(precipitation)          AS monthly_precipitation,
                      SUM(case_total)             AS monthly_case_total,
                  FROM disease_climate
                  WHERE adm3_en = 'Dagupan City'
                    AND disease_icd10_code = 'A90-A91'
                    AND "date" >= '2013-01-01':: DATE
GROUP BY
    DATE_TRUNC('month', "date"),
    EXTRACT (MONTH FROM "date"),
    EXTRACT (YEAR FROM "date")
    )
SELECT
    "month",
    AVG(
            monthly_precipitation) OVER (
    PARTITION BY month_number
    ORDER BY "year"
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS precipitation, AVG(
        monthly_case_total) OVER (
    PARTITION BY month_number
    ORDER BY "year"
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS case_total
FROM smoothed
```

<LineChart
  data={disease_climate}
  x="month"
  y="precipitation"
  y2="case_total"
  yAxisTitle="Precipitation (mm)"
  y2AxisTitle="Dengue cases"
  colorPalette={["blue", "red"]}
>
  {#each Array(2023-2013).fill(0).map((_, i) => i + 2013) as year}
    <ReferenceArea xMin={`${year}-06-01`} xMax={`${year}-08-01`} color="red" />
  {/each}
</LineChart>
