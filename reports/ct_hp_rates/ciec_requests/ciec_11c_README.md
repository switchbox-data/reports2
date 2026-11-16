# CIEC-11(c): CAIRO input and output files

PURA Docket No. 26-05-10. These are the CAIRO input and output files used in the Direct Testimony of Juan-Pablo Velez that were not already provided in Exhibits JPV-3 and JPV-4 or in response to CIEC-1. They come from CAIRO batch `ct_20261015_a`, run with the configuration in [rate-design-platform at commit `e97a3ca`](https://github.com/switchbox-data/rate-design-platform/tree/e97a3ca).

`MANIFEST.csv` lists every file with its size, SHA-256 checksum and download link.

## Outputs

- `outputs/master/<scenario>/comb_bills_year_target/`: customer bills by month and year, one table per scenario.
- `outputs/master/<scenario>/cross_subsidization_BAT_values/`: customer bill alignment results, one table per scenario.
- `outputs/runs/<run>/`: for each CAIRO run, the tariff it billed (`tariff_final_config.json`), its settings (`scenario_settings.json`), and the marginal cost files it read (`marginal_costs_used.json`). Delivery runs also include annual billed kWh (`billing_kwh_annual.parquet`), and the two Rate 1 delivery runs hourly billed kWh (`billing_kwh_8760.parquet`); the other runs' hourly files are identical.

## Inputs

- `inputs/resstock/`: ResStock building metadata, utility assignments, and hourly loads for the 3,539 Eversource buildings (upgrade 00 before the heat pump retrofit, upgrade 02 after).
- `inputs/marginal_costs/`: the hourly distribution and bulk transmission marginal costs.
- `inputs/config/`: tariffs, tariff maps, scenario definitions and revenue requirement settings, as in rate-design-platform at `e97a3ca`.
- `inputs/postprocessing/`: heating oil and propane prices and CPI, used to compute delivered-fuel bills and low-income eligibility in the bill tables.

## Notes

- Timestamps: in `billing_kwh_8760.parquet` they are UTC; subtract five hours for Eastern Standard Time. In the ResStock loads and marginal cost files they are Eastern Standard Time.
- Supply rates are Eversource's 2025 standard service rates, and gas rates are the filed residential tariffs of Connecticut Natural Gas, Southern Connecticut Gas, Yankee Gas and Norwich Public Utilities.
