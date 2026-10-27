# Ameren Illinois TOU and EV sources

Markdown extracts supporting the evaluation of Ameren Illinois's supply time-of-use rate (**Rider STOU**, ICC ERM #26-175, filed Sep 29, 2026, effective Nov 13, 2026; P.A. 104-0458, 220 ILCS 5/16-107.8). The Rider STOU compliance tariff itself is one level up: `../icc_erm_26-175_ameren_rider_stou_compliance_tariff.md`.

The original PDFs are **not stored** in the repo. `MANIFEST.csv` records each PDF's size, page count, text length, SHA-256 and source URL so a file can be re-fetched and verified.

ICC docket pages (`icc.illinois.gov/docket/...`) are CAPTCHA-gated for scripted downloads; the PDFs were pulled through a browser session. e-Tariff PDFs follow `https://icc.illinois.gov/downloads/public/filing/<first digit of id>/<id>.pdf`.

## Contents

| File                                                              | Original PDF (not stored)   | Use for                                                                                                                                            |
| ----------------------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `icc_396837_ameren_retail_supply_informational_filing_mar2026.md` | ICC e-Tariff 396837 (2 pp.) | 118th Informational Sheet: April 2026 supply charges (BGS-1/2/5, RTP, Rider EUA factors). The format Rider STOU informational filings will follow. |
| `icc_398320_ameren_retail_supply_informational_filing_apr2026.md` | ICC e-Tariff 398320 (2 pp.) | 119th Informational Sheet: May 2026 supply charges.                                                                                                |

Delivery-side EV time-of-use material (Rider EVCP / ChargeSmart, FlexCharge, ChargeReady) from Docket P2026-0051 is in [`ev/`](ev/README.md).

## Extraction notes

- Each extract's header lists the extraction method and any notes on what the extractor added (labelled as such), omitted or flagged.
- Bibliographic details not printed on a document (docket petition title, e-docket id, document id) are supplied from the ICC e-docket page and are labelled in the extract's notes.
