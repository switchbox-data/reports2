# ComEd — Guide to the Retail Customers' Billed Delivery Service Charges: Residential Flat and Time-of-Use DFC, Base Charge to Billed Charge (bills beginning October 2026)

**Source**: `comed_guide_billed_delivery_service_charges_oct2026.pdf` (downloaded from `https://azure-na-assets.contentstack.com/v3/assets/blt3ebb3fed6084be2a/blt7904befea93c3525/AGuideToTheRetailCustomersBilledDeliveryServiceCharges.pdf`). The file is not an ICC filing; it is ComEd's own explanatory table on comed.com, and the PDF carries no filing date. The factor values it applies are labelled "beginning with Oct. 2026 bill".
**Pages extracted here**: 2 of 4 (pp. 1–2: residential flat and residential time-of-use). Pages 3–4 (nonresidential delivery classes, lighting) are not extracted.
**Date**: Applies to bills beginning October 2026
**Author(s)**: Commonwealth Edison Company (no individual author)
**Author affiliations**: Commonwealth Edison Company ("ComEd")
**Document type**: Company explainer: "an instructional tool that provides how each delivery charge is calculated from the Base Charge to the charge shown on the bill."
**Extraction method**: Embedded PDF text. The PDF text layer drops empty cells and scrambles the factor header block, so column positions were read from the rendered pages and each row was checked arithmetically (base × factor, and sum of columns against the printed total); the one place where the printed total does not reconcile is flagged inline.

**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- This file **was added beyond the original extraction plan** because it is the only ComEd source that puts the flat DFC and the TOU DFC side by side on the **billed** basis, which resolves the CUB fact-sheet basis problem (see `cub_comed_delivery_tod_fact_sheet_mar2026.md` and `comed/README.md`).
- Column key (source): A = Base Charge; B = Incremental Distribution Uncollectible Cost Factor (IDUF); C = Excess Deferred Income Tax Factor (EDAF); D = Retail Customer Assessment (RCA, Rider RCA; flat tables only); then Determination of Delivery Reconciliation Adjustment (DSPR); Revenue Balancing Adjustment Factor (RBAF); Total Plan Adjustment Factor (TPAF); Distributed Generation Rebate Adjustment (DGRA). On the flat table the letters run A = Base, B = IDUF, C = EDAF, D = RCA, then E = DSPR, F = RBAF, G = TPAF, H = DGRA (extractor mapping of the source's column letters; the source prints letters only for A–D). "Resultant charge beginning with Oct. 2026 bill" = sum of the columns. "—" marks an empty cell in the source.
- Source footnote (2): "Factors are multiplied times the Base Charge with rounding. Single monthly charges and per kilowatt charges are rounded to two decimal places. Charges per kilowatthour are rounded to five decimal places." Footnote (3): Rider RCA combines the Renewable Energy Resources and Coal Technology Development Assistance Charge and the Energy Assistance Charge for the Supplemental Low-Income Energy Assistance Fund (base energy assistance charge times a class-specific multiplier), and also charges a Residential Real Time Pricing Program Cost Recovery Charge to all residential customers. "For more information, please refer to the complete Rider RCA tariff in the Company's Schedule of Rates for Electric Service." Footnote (4): all RBAFs are in the order of the delivery classes listed. Footnote (1): X.XXX denotes a charge and (X.XXX) a credit.
- Dollar signs are escaped as `\$`.

**Factor values applied (Oct. 2026 bills)**:

| Factor                                | Value                                                                            |
| ------------------------------------- | -------------------------------------------------------------------------------- |
| IDUF (residential)                    | 1.0217 (i.e. a 2.17% increment on the base: e.g. \$0.05698 × 0.0217 = \$0.00124) |
| EDAF                                  | 0.00000                                                                          |
| RCA (monthly, customer charge only)   | \$0.91 per month                                                                 |
| DSPR                                  | 0.006785                                                                         |
| TPAF                                  | 0.065510                                                                         |
| DGRA (per kWh, DFC only)              | \$0.00062 per kWh                                                                |
| RBAF, single family, no electric heat | 0.007668                                                                         |
| RBAF, multi family, no electric heat  | 0.011682                                                                         |
| RBAF, single family, electric heat    | 0.069810                                                                         |
| RBAF, multi family, electric heat     | 0.064486                                                                         |

[The four RBAF values are listed in the order of the delivery classes (source footnote 4), without row labels in the text layer. The class assignment was confirmed arithmetically: each reproduces the printed RBAF dollar amounts, e.g. 0.007668 × \$13.26 = \$0.10.]

---

## Table 1, Page 1 — Calculation of Delivery Service Charges for Residential Customers: Flat (non-TOU) charges

| Delivery class                             | Charge                                      | A. Base     | B. IDUF | C. EDAF | D. RCA | DSPR    | RBAF    | TPAF    | DGRA    | Billed      |
| ------------------------------------------ | ------------------------------------------- | ----------- | ------- | ------- | ------ | ------- | ------- | ------- | ------- | ----------- |
| Single Family, Without Electric Space Heat | Customer Charge (\$/mo)                     | 13.26       | 0.29    | 0.00    | 0.91   | 0.09    | 0.10    | 0.87    | —       | 15.52       |
|                                            | Standard Metering Service Charge (\$/mo)    | 3.52        | 0.08    | 0.00    | —      | 0.02    | 0.03    | 0.23    | —       | 3.88        |
|                                            | **Distribution Facilities Charge (\$/kWh)** | **0.05698** | 0.00124 | 0.00000 | —      | 0.00039 | 0.00044 | 0.00373 | 0.00062 | **0.06340** |
|                                            | IEDT (\$/kWh)                               | 0.00124     | 0.00003 | —       | —      | —       | 0.00001 | —       | —       | 0.00128     |
| Multi Family, Without Electric Space Heat  | Customer Charge (\$/mo)                     | 9.76        | 0.21    | 0.00    | 0.91   | 0.07    | 0.11    | 0.64    | —       | 11.70       |
|                                            | Standard Metering Service Charge (\$/mo)    | 3.52        | 0.08    | 0.00    | —      | 0.02    | 0.04    | 0.23    | —       | 3.89        |
|                                            | **Distribution Facilities Charge (\$/kWh)** | **0.04354** | 0.00095 | 0.00000 | —      | 0.00030 | 0.00051 | 0.00285 | 0.00062 | **0.04877** |
|                                            | IEDT (\$/kWh)                               | 0.00124     | 0.00003 | —       | —      | —       | 0.00001 | —       | —       | 0.00128     |
| Single Family, With Electric Space Heat    | Customer Charge (\$/mo)                     | 15.09       | 0.33    | 0.00    | 0.91   | 0.10    | 1.05    | 0.99    | —       | 18.47       |
|                                            | Standard Metering Service Charge (\$/mo)    | 3.52        | 0.08    | 0.00    | —      | 0.02    | 0.25    | 0.23    | —       | 4.10        |
|                                            | **Distribution Facilities Charge (\$/kWh)** | **0.02712** | 0.00059 | 0.00000 | —      | 0.00018 | 0.00189 | 0.00178 | 0.00062 | **0.03218** |
|                                            | IEDT (\$/kWh)                               | 0.00124     | 0.00003 | —       | —      | —       | 0.00009 | —       | —       | 0.00136     |
| Multi Family, With Electric Space Heat     | Customer Charge (\$/mo)                     | 10.57       | 0.23    | 0.00    | 0.91   | 0.07    | 0.68    | 0.69    | —       | 13.15       |
|                                            | Standard Metering Service Charge (\$/mo)    | 3.52        | 0.08    | 0.00    | —      | 0.02    | 0.23    | 0.23    | —       | 4.08        |
|                                            | **Distribution Facilities Charge (\$/kWh)** | **0.02576** | 0.00056 | 0.00000 | —      | 0.00017 | 0.00166 | 0.00169 | 0.00062 | **0.03046** |
|                                            | IEDT (\$/kWh)                               | 0.00124     | 0.00003 | —       | —      | —       | 0.00008 | —       | —       | 0.00135     |

---

## Table 1, Page 2 — Calculation of Delivery Service Charges for Residential Customers: Time-of-Use DFC (\$/kWh)

Resultant charge beginning with Oct. 2026 bill = sum of columns (A through G; no RCA column on the TOU table).

| Delivery class                             | Period       | A. Base     | B. IDUF | C. EDAF | DSPR    | RBAF    | TPAF                              | DGRA    | Billed      |
| ------------------------------------------ | ------------ | ----------- | ------- | ------- | ------- | ------- | --------------------------------- | ------- | ----------- |
| Single Family, Without Electric Space Heat | Morning      | 0.04009     | 0.00087 | 0.00000 | 0.00027 | 0.00031 | 0.00263                           | 0.00062 | 0.04479     |
|                                            | Mid-Day Peak | **0.10712** | 0.00233 | 0.00000 | 0.00073 | 0.00082 | 0.00702                           | 0.00062 | **0.11864** |
|                                            | Evening      | 0.03747     | 0.00081 | 0.00000 | 0.00025 | 0.00029 | 0.00245                           | 0.00062 | 0.04189     |
|                                            | Overnight    | 0.02984     | 0.00065 | 0.00000 | 0.00020 | 0.00023 | 0.00195                           | 0.00062 | 0.03349     |
| Multi Family, Without Electric Space Heat  | Morning      | 0.03073     | 0.00067 | 0.00000 | 0.00021 | 0.00036 | 0.00201                           | 0.00062 | 0.03460     |
|                                            | Mid-Day Peak | 0.08689     | 0.00189 | 0.00000 | 0.00059 | 0.00102 | 0.00569                           | 0.00062 | 0.09670     |
|                                            | Evening      | 0.02856     | 0.00062 | 0.00000 | 0.00019 | 0.00033 | 0.00187                           | 0.00062 | 0.03219     |
|                                            | Overnight    | 0.02251     | 0.00049 | 0.00000 | 0.00015 | 0.00026 | — **[TPAF cell empty in source]** | 0.00062 | 0.02403     |
| Single Family, With Electric Space Heat    | Morning      | 0.01999     | 0.00043 | 0.00000 | 0.00014 | 0.00140 | 0.00131                           | 0.00062 | 0.02389     |
|                                            | Mid-Day Peak | 0.05329     | 0.00116 | 0.00000 | 0.00036 | 0.00372 | 0.00349                           | 0.00062 | 0.06264     |
|                                            | Evening      | 0.01890     | 0.00041 | 0.00000 | 0.00013 | 0.00132 | 0.00124                           | 0.00062 | 0.02262     |
|                                            | Overnight    | 0.01550     | 0.00034 | 0.00000 | 0.00011 | 0.00108 | 0.00102                           | 0.00062 | 0.01867     |
| Multi Family, With Electric Space Heat     | Morning      | 0.01925     | 0.00042 | 0.00000 | 0.00013 | 0.00124 | 0.00126                           | 0.00062 | 0.02292     |
|                                            | Mid-Day Peak | 0.04975     | 0.00108 | 0.00000 | 0.00034 | 0.00321 | 0.00326                           | 0.00062 | 0.05826     |
|                                            | Evening      | 0.01823     | 0.00040 | 0.00000 | 0.00012 | 0.00118 | 0.00119                           | 0.00062 | 0.02174     |
|                                            | Overnight    | 0.01512     | 0.00033 | 0.00000 | 0.00010 | 0.00098 | 0.00099                           | 0.00062 | 0.01814     |

**Source inconsistency to be aware of**: the multi-family, no-electric-heat Overnight row has no TPAF amount in the source, and its printed total (0.02403) equals the sum of the other columns. Applying the same TPAF (0.065510 × 0.02251 ≈ 0.00147) as every other row would give a billed rate of about 0.02550. Whether the 0.02403 is a table omission or the tariff intent has not been checked against the tariff sheets; the other fifteen TOU rows reconcile exactly.

---

**Reading guide (added by extractor, not source text)**: On the **billed** basis (Oct. 2026 factors), the residential flat DFC is 6.340 ¢/kWh (single family, no electric heat), 4.877 (multi family, no heat), 3.218 (single family, electric heat) and 3.046 (multi family, electric heat). The corresponding TOU DFCs run from 3.349 ¢ (overnight) to 11.864 ¢ (mid-day peak) for the single-family, no-heat class. The billed-to-base uplift on the flat DFC is 11.3% (single family, no heat), 12.0% (multi family, no heat), 18.7% (single family, heat) and 18.2% (multi family, heat); electric-heat classes carry a much larger RBAF (about 7% vs under 1.2%).
