# ComEd Ex. 17.04 — Capacity Charge Determination (kW-based Monthly Capacity Charge, MCC), Strawman Proposal (Rehearing Direct)

**Source**: `icc_636690_ex_17_04_mcc_kw_charge_illustrative.pdf` (ICC e-docket file id / filing id 636690)
**Pages**: 1 (spreadsheet-rendered workbook, landscape)
**Date**: April 4, 2025 (date of ComEd Ex. 17.0, the rehearing direct testimony with which this exhibit was filed; no date is printed on the exhibit itself)
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), On Rehearing
**Author(s)**: ComEd (sponsored by Kathleen E. Kremer, Principal Rate Analyst, Retail Rates)
**Document type**: Illustrative exhibit (spreadsheet workpaper printout)
**ComEd exhibit no.**: ComEd Ex. 17.04
**Extraction method**: Embedded PDF text (PyMuPDF), table verified against the rendered page image
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- The printed header block ("ICC Docket No. 24-0378 (On Rehearing) / ComEd Ex. 17.04") is omitted; this one-page exhibit carries no "Page N of N" line. The "Illustrative Example" label and the placeholder "MONTH 20YY" dates are kept.
- Column letters and formulas are reproduced as printed; spreadsheet footnotes are given as a "Notes" block directly under the table (no markdown footnote syntax). Blue "input" font colors are not transcribed.
- Arithmetic cross-check: 270.43 × 365 ÷ 12 ÷ 1,000 = 8.22567 ✓; 8.22567 × 1.0128 = 8.33096 ✓; 8.33096 × 1.0053 = 8.37511 ✓.

**Differences vs compromise exhibit**: This exhibit has **no counterpart in the Compromise Proposal** (there is no Ex. 19.04). It is the strawman's separate **kW-based Monthly Capacity Charge (MCC)**: **8.37511 \$/kW-month** after uncollectible factors (8.22567 before), derived from the PJM Net Load Price of 270.43 \$/MW-day for the ComEd Zone, 2025/2026 delivery year. In the compromise, capacity is instead recovered 100% in the Mid-Day Peak kWh rate (Ex. 19.0 at 3:49–54; Ex. 19.02 page 2): capacity cost of \$602,456 allocated 100% to the Mid-Day Peak period over 4,566,998 Mid-Day Peak kWh (2,012,553 summer + 2,554,445 nonsummer) = 13.192 ¢/kWh before uncollectible factors, i.e. 13.432 ¢/kWh after SBUF (1.0128) and ISUF (1.0053) — which is why the compromise Mid-Day Peak charge is 18.219 / 16.814 ¢/kWh versus the strawman's energy-only 4.787 / 3.383 ¢/kWh (Ex. 17.03).

---

## Capacity Charge Determination

**Commonwealth Edison Company — Capacity Charge Determination — Applicable to Retail Customers Served Under Rate BEST (1)** (_Illustrative Example_)

**For Application Beginning with the MONTH 20YY Monthly Billing Period and Extending Through the MONTH 20YY Monthly Billing Period.**

<!-- EPON: capacity-mdppec — strawman capacity recovery as a separate kW charge: Monthly Capacity Charge 8.37511 $/kW-month from PJM NLP 270.43 $/MW-day (2025/26 ComEd Zone); contrast with compromise where 100% of capacity is in the Mid-Day Peak kWh rate -->

| a: NLP \$/MW-Day (2) | b: Days in the Billing Periods | c: Monthly Billing Periods | d = a * b / c / 1000: MCC prior to including Uncollectible Factor \$/kW-Month | e: SBUF (3) | f = d * e: MCC w/ SBUF \$/kW-Month (4) | g: ISUF (5) | h = f * g: MCC w/ SBUF and ISUF \$/kW-Month (6) (7) |
| -------------------: | -----------------------------: | -------------------------: | ----------------------------------------------------------------------------: | ----------: | -------------------------------------: | ----------: | --------------------------------------------------: |
|               270.43 |                            365 |                         12 |                                                                       8.22567 |      1.0128 |                                8.33096 |      1.0053 |                                         **8.37511** |

Notes:

1. Rate BEST - Basic Electric Service Time Of Use (Rate BEST).
2. The Net Load Price (NLP) for the ComEd Zone for the 2025/2026 delivery year posted on PJM's web site on August 16, 2024: [PJM RPM page](https://www.pjm.com/markets-and-operations/rpm.aspx)
3. Residential Supply Base Uncollectible Cost Factor (SBUF<sub>R</sub>) determined in accordance with Rider UF - Uncollectible Factors (Rider UF) listed in Informational Sheet No. 21.
4. SBUF<sub>R</sub> applied pursuant to Rate BEST.
5. Residential Incremental Supply Uncollectible Cost Factor (ISUF<sub>sys</sub>) listed in Informational Sheet No. 20.
6. ISUF<sub>R</sub> applied pursuant to Rate BEST.
7. Subject to rounding.
