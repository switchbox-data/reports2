"""Load monthly residential heating fuel prices from EIA data on S3."""

from __future__ import annotations

import polars as pl


def load_monthly_fuel_prices(path_root: str, state: str, year: int) -> pl.DataFrame:
    """Load monthly residential oil + propane prices for a state/year."""
    root = path_root.rstrip("/") + "/"
    df = (
        pl.scan_parquet(root)
        .filter((pl.col("year") == year) & (pl.col("state") == state) & (pl.col("price_type") == "residential"))
        .select(
            pl.col("month").cast(pl.Int8),
            pl.col("product"),
            pl.col("price_per_gallon"),
        )
        .collect()
    )
    pivoted = df.pivot(on="product", index="month", values="price_per_gallon")
    for col in ("heating_oil", "propane"):
        assert col in pivoted.columns, f"Missing '{col}' in EIA fuel prices for state={state}, year={year}"
    result = pivoted.select(
        pl.col("month"),
        pl.col("heating_oil").alias("oil_price_per_gallon"),
        pl.col("propane").alias("propane_price_per_gallon"),
    )
    assert result.filter(
        pl.col("oil_price_per_gallon").is_null() | pl.col("propane_price_per_gallon").is_null()
    ).is_empty(), f"Null fuel prices for state={state}, year={year}"
    return result
