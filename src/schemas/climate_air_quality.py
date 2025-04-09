import polars as pl

ClimateAirQuality = pl.Struct(
    [
        pl.Field("uuid", pl.String()),
        pl.Field("adm4_pcode", pl.String()),
        pl.Field("date", pl.Date()),
        pl.Field("freq", pl.Enum(["D"])),
        pl.Field("no2", pl.Float32()),
        pl.Field("co", pl.Float32()),
        pl.Field("so2", pl.Float32()),
        pl.Field("o3", pl.Float32()),
        pl.Field("pm10", pl.Float32()),
        pl.Field("pm25", pl.Float32()),
    ]
)
