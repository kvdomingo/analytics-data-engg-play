# Open Viz

## Visualizing precipitation and dengue cases peaks in Dagupan

```sql disease_climate
SELECT *
FROM disease_climate
WHERE adm3_en = 'Dagupan City'
  AND disease_icd10_code = 'A90-A91'
  AND "date" >= '2013-01-01':: DATE
```

<LineChart
  title="precipitation"
  data={disease_climate}
  x="date"
  y="case_total"
  y2="precipitation"
  yAxisTitle="Precipitation (mm)"
  y2AxisTitle="Dengue cases"
/>
