---
source_file: heatfx2026final.pdf
citekey: isone_Final2026Heat_2026
zotero_item: "ZR7KUNF3"
public_url: https://drive.google.com/file/d/1UXx_NjDWlhs4MIHJGfHQ_vOw9u5wlFwn/view
short_url: https://pub.switch.box/isone_Final2026Heat_2026
source_url: https://www.iso-ne.com/static-assets/documents/100034/heatfx2026final.pdf
md5: "d4c0f403666141b52589f19ee150a228"
validated: 2026-11-05
filing_date: 2026-05-01
filer: ISO New England (ISO-NE)
document_type: presentation (slide deck)
pages_total: 26
extraction_scope: full
citation_scheme: page
context: ISO New England's Final 2026 Heat Pump Forecast, published May 1, 2026, projecting heat pump adoption and the resulting energy and peak demand across New England.
contents: A 26-page public slide deck. The residential space-heating table, Annual Incremental Increase in HP Stock (1,000 Housing Units), gives Connecticut 8, 9, 10, 12, and 14 thousand housing units in 2027 through 2031.
why_here: Those Connecticut additions, times Eversource's share of the RASS population frame, are the CIEC-1(c) enrollment ceiling.
---

# Final 2026 Heat Pump Forecast

**Source**: heatfx2026final.pdf
**Pages**: 26 (PowerPoint slide deck; PDF page N is slide N)
**Date**: May 1, 2026 (printed on slide 1); PDF creation date 2026-04-29 (PDF metadata, not printed on the slides)
**Author(s)**: ISO New England (no individual authors named). The PDF metadata has no title or author.
**Author affiliations**: not printed in the PDF beyond the ISO New England logo.

_Extractor note (not source text): The printed slide number appears in a green box at the lower right of each slide and also as "ISO-NE PUBLIC N" in the text layer; every `printed p.` value below is that slide number. Minor typographical errors in the source were not corrected; the one apparent typo ("Aikin") is kept and marked `[sic]`. Page-level text in the PDF is slide text, transcribed in reading order; charts are described in `[DIAGRAM DESCRIPTION]` blocks. Numeric values in tables are as printed. All slide numbers in the PDF's running footers ("ISO-NE PUBLIC") are omitted._

---

[PDF p. 1 | printed p. 1]

MAY 1, 2026

# Final 2026 Heat Pump Forecast

ISO-NE PUBLIC

[DIAGRAM DESCRIPTION: Title slide artwork]

ISO New England logo (stylized New England map made of orange dots, "ISO new england") at left of the title. A decorative illustration along the bottom shows a transmission tower, solar panels, wind turbines (onshore and offshore), a house with rooftop solar and an electric vehicle charging, and water, above a dark circuit-board band. Decorative only.

[PDF p. 2 | printed p. 2]

# Acronyms

| Acronym | Meaning                        | Acronym | Meaning                                   |
| ------- | ------------------------------ | ------- | ----------------------------------------- |
| BTMPV   | Behind-the-meter Photovoltaics | CELT    | Capacity, Energy, Loads, and Transmission |
| COP     | Coefficient of Performance     | EV      | Electric Vehicle                          |
| GHG     | Greenhouse Gas                 | GSHP    | Ground Source Heat Pump                   |
| GWh     | Gigawatt Hour                  | HP      | Heat Pump                                 |
| MW      | Megawatt                       | NREL    | National Renewable Energy Laboratory      |
| PTHP    | Packaged Terminal Heat Pump    | RUT     | Rooftop Unit                              |
| SF      | Square Feet                    | VRF     | Variable Refrigerant Flow                 |

_Extractor note (not source text): "RUT" is printed as shown; other slides use "RTU" for rooftop unit._

[PDF p. 3 | printed p. 3]

# Outline

- Introduction
- Heat Pump Adoption Forecast
- Hourly Demand Modeling Methodology
- Energy and Peak Demand Forecast

[PDF p. 4 | printed p. 4]

# Introduction

- The heat pump (HP) forecast reflects the anticipated energy and demand impacts of electrifying space heating and water heating across residential and commercial buildings in New England
  - These impacts are included as part of the 2026 Capacity, Energy, Loads, and Transmission (CELT) forecast
- The methodology used to model and forecast heating electrification impacts remains relatively unchanged from the [CELT 2025 forecast cycle (slides 29-71)](https://www.iso-ne.com/static-assets/documents/100023/heat_fx_2025.pdf):
  1. Adoption forecasting
     - Forecasts adoption of residential and commercial space and water heating electrification technologies at the county level considering building stock characteristics, state policy, and economic factors
     - Adoption pathways consist of unique combinations of building type, legacy fuel, and displacement level
  2. Hourly demand modeling
     - Captures the electricity demand impacts of HP adoption
  3. Energy and peak demand calculation
     - Energy stems from a direct summation of simulated hourly demand
     - Peak demand is derived from a "waterfall" approach, considering all load forecast components
     - Peak demand and monthly energy incorporate gross-ups to account for transmission and distribution losses

[PDF p. 5 | printed p. 5]

# Updates to the HP Forecast for CELT 2026

- For CELT 2026, the HP adoption forecast was reduced by 5% across all sectors and heating types
  - Detailed on slide 5 of the November 7, 2025 [Update on Heat Pump Forecast Enhancements](https://www.iso-ne.com/static-assets/documents/100029/lf2026_hpfx_updates.pdf) presentation
- Building space heating demand parameters were reduced by 15% for residential and 5% for commercial applications to reflect the impact of weatherization
  - Discussed on slide 6 of the November 7, 2025 [Update on Heat Pump Forecast Enhancements](https://www.iso-ne.com/static-assets/documents/100029/lf2026_hpfx_updates.pdf) presentation
- Maximum heating demand parameters were reduced by 10% in full displacement modeling to reflect less resistance backup heat
  - Discussed on slide 7 of the November 7, 2025 [Update on Heat Pump Forecast Enhancements](https://www.iso-ne.com/static-assets/documents/100029/lf2026_hpfx_updates.pdf) presentation

[PDF p. 6 | printed p. 6]

# Heating Electrification Forecast Process

[DIAGRAM DESCRIPTION: Heating Electrification Forecast Process]

A flow diagram with two horizontal swim lanes feeding two output boxes at right.

- **Top lane (purple): adoption.** Box "County-Level Existing Building Stock" flows rightward through a node that also takes in "Heating Electrification Pathways", then through a second node that also takes in "Market Segmentation Parameters", into the box "**Heat Pump Adoption Forecast** (_By Sector, Pathway, Building, & County_)".
- **Bottom lane (blue): hourly demand.** Box "NREL Databse [sic] (ResStock/ComStock)" flows rightward through a node that also takes in "Building Heating Demand", then a node taking "Heat Pump COP Curves", then a node taking "County-Level Weather Profile", into the box "**Unitized Hourly Demand Simulations** (_By Sector, Pathway, Building, & County_)".
- The two result boxes merge at a gray node, which splits into two outputs:
  - "**Hourly Residential Forecast**": 5 Building Types × 67 Counties; _6 Space Heating Pathways_; _1 Water Heating Pathway_.
  - "**Hourly Commercial Forecast**": 14 Building Types × 67 Counties; _9 Space Heating Pathways_; _2 Water Heating Pathways_.

[→ See original PDF page 6 for visual rendering]

[PDF p. 7 | printed p. 7]

# HEAT PUMP ADOPTION FORECAST

[PDF p. 8 | printed p. 8]

# Residential Space Heating Adoption

**Annual Incremental Increase in HP Stock (1,000 Housing Units)**

| Year                                | CT      | MA      | ME      | NH     | RI     | VT      | NE        |
| ----------------------------------- | ------- | ------- | ------- | ------ | ------ | ------- | --------- |
| 2026                                | 7       | 33      | 16      | 4      | 3      | 10      | 73        |
| 2027                                | 8       | 38      | 17      | 4      | 3      | 11      | 81        |
| 2028                                | 9       | 44      | 18      | 5      | 4      | 11      | 89        |
| 2029                                | 10      | 49      | 19      | 5      | 4      | 11      | 98        |
| 2030                                | 12      | 56      | 20      | 6      | 5      | 11      | 109       |
| 2031                                | 14      | 63      | 23      | 7      | 6      | 11      | 123       |
| 2032                                | 17      | 66      | 25      | 7      | 7      | 10      | 132       |
| 2033                                | 21      | 68      | 26      | 9      | 8      | 10      | 141       |
| 2034                                | 25      | 69      | 26      | 10     | 10     | 10      | 145       |
| 2035                                | 28      | 75      | 28      | 12     | 11     | 11      | 164       |
| **Cumulative Adoption (2026-2035)** | **150** | **561** | **217** | **67** | **60** | **106** | **1,161** |

_Extractor note (not source text): The column sums of the printed annual rows differ slightly from the printed "Cumulative Adoption" row for some columns (Connecticut annual values sum to 151 vs. printed 150; NH 69 vs. 67; RI 61 vs. 60; ME 218 vs. 217; NE 1,155 vs. 1,161; MA 561 and VT 106 match). The printed 2034 NE value (145) is also lower than the sum of that row's state values (150). Values are kept exactly as printed; the differences are consistent with rounding in the source but the 2034 NE row is larger than rounding would explain._

[DIAGRAM DESCRIPTION: Cumulative HP Stock (1,000 Housing Units) — residential space heating]

Left side of the slide: a 2-column × 3-row grid of small line charts titled "Cumulative HP Stock (1,000 Housing Units)", one panel each for CT, MA, ME, NH, RI and VT, plus a wide stacked-area chart for New England below. In each state panel the x-axis is year (2025 to 2050, ticks every 5 years) and the y-axis is "# Housing Units (1000s)". Each panel has two lines: a solid red line for **CELT 2026** and a dashed black line for **CELT 2025**. All lines rise from near zero in 2025 in an S-shaped curve; the CELT 2026 line sits at or slightly below the CELT 2025 line in every state, with the gap widest in VT and ME. Approximate y-axis scale (tick marks): CT up to about 500+ (curves end near 650 in 2050), MA ticks 0, 1,000, 2,000 (curves end near 1,600), ME ticks 0 and 500 (curves end near 480-500), NH ticks 0 to 400 (curves end near 340-360), RI ticks 0 and 200 (curves end near 290-300), VT ticks 0 and 200 (curves end near 190-210, flattening after about 2040). The wide "New England" panel is a stacked-area chart (x: 2025-2050; y: "# Housing Units (1000s)", ticks 0, 2,000, 4,000) with layers from bottom to top: CT (light blue), MA (purple), ME (yellow), NH (red), RI (green), VT (gray), reaching about 3,500 thousand housing units in total by 2050. The legend for the line charts reads "CELT 2026" (solid red) and "CELT 2025" (dashed black). Values are read from the rendered chart and are approximate; the table above holds the printed numbers.

[→ See original PDF page 8 for visual rendering]

[PDF p. 9 | printed p. 9]

# Residential Water Heating Adoption

**Annual Incremental Increase in HP Stock (1,000 Housing Units)**

| Year                                | CT      | MA      | ME     | NH     | RI     | VT     | NE      |
| ----------------------------------- | ------- | ------- | ------ | ------ | ------ | ------ | ------- |
| 2026                                | 4       | 9       | 3      | 2      | 1      | 1      | 19      |
| 2027                                | 5       | 11      | 3      | 2      | 1      | 1      | 24      |
| 2028                                | 6       | 14      | 4      | 2      | 2      | 2      | 29      |
| 2029                                | 7       | 18      | 6      | 2      | 2      | 2      | 37      |
| 2030                                | 9       | 23      | 7      | 3      | 2      | 3      | 47      |
| 2031                                | 11      | 29      | 9      | 3      | 3      | 4      | 58      |
| 2032                                | 14      | 35      | 12     | 3      | 4      | 5      | 71      |
| 2033                                | 16      | 42      | 13     | 4      | 4      | 6      | 85      |
| 2034                                | 18      | 51      | 16     | 4      | 5      | 7      | 102     |
| 2035                                | 22      | 60      | 19     | 5      | 6      | 8      | 119     |
| **Cumulative Adoption (2026-2035)** | **112** | **291** | **90** | **29** | **30** | **39** | **592** |

[DIAGRAM DESCRIPTION: Cumulative HP Stock (1000 Housing Units) — residential water heating]

Left side of the slide: the same layout as slide 8, titled "Cumulative HP Stock (1000 Housing Units)": six small line panels (CT, MA, ME, NH, RI, VT; x: 2025-2050; y: "# Housing Units (1000s)") each with a solid blue line for **CELT 2026** and a dashed black line for **CELT 2025**, and a wide stacked-area "New England" panel below. In every panel the curves rise slowly then steeply after about 2035 and the CELT 2026 line sits very slightly below (or on top of) the CELT 2025 line. Approximate end-of-2050 levels: CT about 700-800 (tick 500 shown), MA about 1,600 (ticks 0, 1,000, 2,000), ME about 400-450, NH about 230-250, RI about 210-230, VT about 180-190. The New England stacked-area panel (layers bottom to top CT light blue, MA purple, ME yellow, NH red, RI green, VT gray; y ticks 0, 2,000, 4,000) reaches about 3,500 thousand housing units by 2050. Values read from the rendered chart are approximate.

[→ See original PDF page 9 for visual rendering]

[PDF p. 10 | printed p. 10]

# Commercial Space Heating Adoption

**Annual Incremental Increase in Floor Space (Million Sq Ft.)**

| Year                                | CT      | MA      | ME     | NH     | RI     | VT     | NE      |
| ----------------------------------- | ------- | ------- | ------ | ------ | ------ | ------ | ------- |
| 2026                                | 10      | 26      | 6      | 3      | 3      | 1      | 47      |
| 2027                                | 10      | 29      | 6      | 3      | 3      | 1      | 52      |
| 2028                                | 11      | 32      | 7      | 3      | 3      | 2      | 58      |
| 2029                                | 12      | 36      | 8      | 4      | 3      | 2      | 65      |
| 2030                                | 15      | 40      | 8      | 4      | 4      | 2      | 75      |
| 2031                                | 18      | 48      | 10     | 5      | 5      | 3      | 89      |
| 2032                                | 21      | 54      | 12     | 5      | 6      | 3      | 101     |
| 2033                                | 25      | 60      | 13     | 6      | 7      | 4      | 115     |
| 2034                                | 28      | 61      | 13     | 6      | 7      | 5      | 120     |
| 2035                                | 30      | 63      | 13     | 7      | 7      | 5      | 125     |
| **Cumulative Adoption (2026-2035)** | **181** | **449** | **96** | **46** | **48** | **28** | **847** |

[DIAGRAM DESCRIPTION: Cumulative Electrified Floor Space (Million Sq Ft.) — commercial space heating]

Left side of the slide: six small line panels (CT, MA, ME, NH, RI, VT; x: 2025-2050; y: "Floor Space (Million Sq Ft.)"), titled "Cumulative Electrified Floor Space (Million Sq Ft.)", each with a solid purple line for **CELT 2026** and a dashed black line for **CELT 2025**; the CELT 2026 line is at or slightly below CELT 2025 throughout. Approximate end-of-2050 levels: CT about 550-600, MA about 1,250, ME about 230-250, NH about 200, RI about 160-170, VT about 75-80. A wide "New England" stacked-area panel below (layers bottom to top CT light blue, MA purple, ME yellow, NH red, RI green, VT gray; y: "Floor Space (Million Sq Ft.)", ticks 0 and 2,000) reaches roughly 2,400 million sq ft by 2050. Values read from the rendered chart are approximate.

[→ See original PDF page 10 for visual rendering]

[PDF p. 11 | printed p. 11]

# Commercial Water Heating Adoption

**Annual Incremental Increase in Floor Space (Million Sq Ft.)**

| Year                                | CT     | MA      | ME     | NH    | RI     | VT    | NE      |
| ----------------------------------- | ------ | ------- | ------ | ----- | ------ | ----- | ------- |
| 2026                                | 1      | 3       | 1      | <1    | 1      | <1    | 6       |
| 2027                                | 1      | 4       | 1      | <1    | 1      | <1    | 7       |
| 2028                                | 2      | 5       | 1      | 1     | 1      | <1    | 9       |
| 2029                                | 2      | 7       | 1      | 1     | 1      | <1    | 11      |
| 2030                                | 2      | 8       | 1      | 1     | 1      | <1    | 14      |
| 2031                                | 3      | 11      | 2      | 1     | 1      | 1     | 18      |
| 2032                                | 3      | 14      | 3      | 1     | 2      | 1     | 23      |
| 2033                                | 4      | 17      | 3      | 1     | 2      | 1     | 28      |
| 2034                                | 5      | 20      | 4      | 1     | 2      | 1     | 33      |
| 2035                                | 6      | 23      | 4      | 2     | 3      | 1     | 38      |
| **Cumulative Adoption (2026-2035)** | **30** | **111** | **20** | **9** | **13** | **5** | **188** |

[DIAGRAM DESCRIPTION: Cumulative Electrified Floor Space (Million Sq Ft.) — commercial water heating]

Left side of the slide: six small line panels (CT, MA, ME, NH, RI, VT; x: 2025-2050; y: "Floor Space (Million Sq Ft.)"), titled "Cumulative Electrified Floor Space (Million Sq Ft.)", each with a solid green line for **CELT 2026** and a dashed black line for **CELT 2025**; the CELT 2026 line is at or slightly below CELT 2025. Approximate end-of-2050 levels: CT about 180-190, MA about 520-540, ME about 60-65, NH about 60-65, RI about 75, VT about 19-20. A wide "New England" stacked-area panel below (layers bottom to top CT light blue, MA purple, ME yellow, NH red, RI green, VT gray; y ticks 0, 500, 1,000) reaches roughly 900 million sq ft by 2050. Values read from the rendered chart are approximate.

[→ See original PDF page 11 for visual rendering]

[PDF p. 12 | printed p. 12]

# Fossil Fuel Displacement

_New England – Residential Space Heating_

> - Each band represents adoption for combinations of heating fuel and displacement type relative to the total New England Housing stock
> - Forecast projects fossil fuels displaced by heat pumps will account for about 58% of total residential housing stock (c. 2022) by 2050
> - Heat pump adoption primarily displaces fuel oil and natural gas

[DIAGRAM DESCRIPTION: Penetration of Electrified Residential Space Heating (NE)]

A stacked-area chart. X-axis: year, 2025 to 2050. Y-axis: "Penetration (% of Housing Stock)", 0 to 60. Six stacked bands, bottom to top: Fuel Oil – Partial (light blue), Fuel Oil – Full (dark blue), Propane – Partial (light orange), Propane – Full (dark orange), Natural Gas – Partial (light green), Natural Gas – Full (dark green). The total rises from about 1% in 2026 to about 57% in 2050 (consistent with the "about 58%" in the text), with a steepening slope through about 2040 and flattening afterward. Approximate 2050 band boundaries read from the chart: Fuel Oil – Partial to about 13%, Fuel Oil – Full to about 28%, Propane – Partial to about 30%, Propane – Full to about 32%, Natural Gas – Partial to about 44%, Natural Gas – Full to about 57%. Fuel oil and natural gas bands are the largest; propane bands are thin. Values read from the rendered chart are approximate.

[→ See original PDF page 12 for visual rendering]

[PDF p. 13 | printed p. 13]

# Fossil Fuel Displacement

_New England – Commercial Space Heating_

> - Each band represents adoption for combinations of heating fuel and displacement type relative to the total New England commercial building stock
> - Forecast projects fossil fuels displaced by heat pumps will account for about 52% of total commercial building space (c. 2022) by 2050
> - Heat pump adoption primarily displaces fuel oil and natural gas

[DIAGRAM DESCRIPTION: Penetration of Electrified Commercial Space Heating (NE)]

A stacked-area chart. X-axis: year, 2025 to 2050. Y-axis: "Penetration (% of Commercial Floor Space)", 0 to 60. Six stacked bands, bottom to top: FuelOil – Partial (light blue), FuelOil – Full (dark blue), Propane – Partial (light orange), Propane – Full (dark orange), NaturalGas – Partial (light green), NaturalGas – Full (dark green). The total rises from about 1% in 2026 to about 52-53% in 2050, nearly linear after about 2030. Approximate 2050 band boundaries: FuelOil – Partial to about 7%, FuelOil – Full to about 22%, Propane – Partial to about 24%, Propane – Full to about 29%, NaturalGas – Partial to about 36%, NaturalGas – Full to about 52%. The natural gas – full band is proportionally larger than in the residential chart. Values read from the rendered chart are approximate.

[→ See original PDF page 13 for visual rendering]

[PDF p. 14 | printed p. 14]

# HOURLY MODELING METHODOLOGY

[PDF p. 15 | printed p. 15]

# Hourly Demand Forecast Overview

- The methodology to model hourly HP demand aligns with the CELT 2025 forecast
  - See slides 29-37 and 64-71 of the [CELT 2025 Heat Pump Forecast](https://www.iso-ne.com/static-assets/documents/100023/heat_fx_2025.pdf) for further details
- Hourly electricity demand is developed across all hours of the 70-year weather simulation period, for each combination of sector, heating type, and pathway

[DIAGRAM DESCRIPTION: Three-step hourly demand modeling process]

Three numbered light-blue boxes in a row, each with its inputs or assumptions listed beneath.

1. **Develop relationships between hourly heating usage and outdoor temperature for all building types.** Inputs: NREL's ResStock and ComStock databases.
2. **Convert heating usage to electricity demand using reference HPs' coefficients of performance (COP).** Inputs: Relationship between temperature and HP efficiency, $COP = \frac{Heat\ Output}{Input\ Power}$.
3. **Develop HP electrical demand models.** Assumptions: Space heating occurs at temperatures below 62°F; each combination of building type and heating pathway modeled separately.

[→ See original PDF page 15 for visual rendering]

[PDF p. 16 | printed p. 16]

# Modeling Inputs

_Reference HPs_

| Sector      | Pathway                                       | Min. Temp. | Heating Supplied (%) |
| ----------- | --------------------------------------------- | ---------- | -------------------- |
| Commercial  | Trane ACX (Air-to-Water)                      | 0          | 100                  |
| Commercial  | Rheem Renaissance Packaged HP (RTU)           | 0          | 81                   |
| Commercial  | Lennox Central HP (Ducted Full)               | 5          | 100                  |
| Commercial  | Lennox Central HP (Ducted Partial)            | 5          | 61-74                |
| Commercial  | Mitsubishi M-Series (Ductless Full)           | -13        | 100                  |
| Commercial  | Daikin DZ6VS (Ductless Partial)               | 5          | 63-76                |
| Commercial  | Energy Star rated models (GSHP)               | -20        | 100                  |
| Commercial  | Rheem Renaissance Packaged HP (RTU – Full)    | 0          | 100                  |
| Commercial  | Rheem Renaissance Packaged HP (RTU – Partial) | 0          | 81                   |
| Commercial  | Mitsubishi M-Series (VRF)                     | -13        | 100                  |
| Residential | Taco Comfort System M (Air-to-Water)          | -5         | 100                  |
| Residential | Lennox Central Heat Pump (Ducted Full)        | 5          | 100                  |
| Residential | Lennox Central Heat Pump (Ducted Partial)     | 5          | 63-74                |
| Residential | Mitsubishi M-Series (Ductless Full)           | -13        | 100                  |
| Residential | Aikin [sic] DZ6VS (Ductless Partial)          | -13        | 65-76                |
| Residential | Energy Star rated models (GSHP)               | -20        | 100                  |
| Residential | ICE-AIR HP (PTHP)                             | 5          | 81                   |

_Extractor note (not source text): The "Min. Temp." column has no unit printed; the COP charts on this slide use °F for temperature._

[DIAGRAM DESCRIPTION: Commercial Pathway COP Curves and Residential Pathway COP Curves]

Two line charts on the left of the slide showing coefficient of performance (COP, y-axis, 0 to 7) against outdoor temperature (x-axis, "Temperature, °F").

- **Commercial Pathway COP Curves** (x-axis about 0 to 47 °F). Legend: Ducted, Full/Part; VRF and Ductless, Full; Ductless, Part; Air-to-Water, Full; RTU, Full/Part and Dual Fuel HP; GSHP. All curves rise with temperature except GSHP, which is flat at about 4. VRF and Ductless Full rises from about 2.4 at 5°F to about 6 at 47°F; Ductless Part from about 2 to about 4.9; Ducted Full/Part from about 1.7 to about 4; RTU from about 2.9 at 0°F to about 3.9 at 47°F; Air-to-Water from about 1.3 to about 2.2.
- **Residential Pathway COP Curves** (x-axis about 5 to 47 °F). Legend: Ducted, Full/Part; Ductless, Full; Ductless, Part; GSHP, Full; Air-to-Water, Full; PTHP, Full/Part. GSHP is flat at about 4. Ductless Full rises from about 2.4 at 5°F to about 6 at 47°F; Ductless Part from about 2 to about 4.9; Ducted Full/Part from about 1.7 to about 4; Air-to-Water starts near 1.9, dips to about 1.8 near 17°F, then rises to about 4.6 at 47°F; PTHP from about 2 to about 3.9.

Values read from the rendered charts are approximate.

[→ See original PDF page 16 for visual rendering]

[PDF p. 17 | printed p. 17]

# Typical Seasonal Load Shapes

_New England in Forecast Year 2040 by Sector and Heating Type_

> - Seasonal profiles highlight the effects of HP operation across the day and in varied weather conditions
> - Space heating applications typically peak in the morning and may experience a second, smaller peak in the evening
> - HP demand in the summer results solely from water heating applications

[DIAGRAM DESCRIPTION: Seasonal HP load shapes, New England, forecast year 2040, by sector and heating type]

Four stacked-area charts (2×2 grid): Spring, 2040; Summer, 2040; Fall, 2040; Winter, 2040. X-axis is hour of day (1 to 24); y-axis is "Demand (MW)". Stack layers from bottom to top: Commercial Space Heating (purple), Commercial Water Heating (light blue), Residential Space Heating (dark blue), Residential Water Heating (orange).

- **Spring, 2040** (y up to 2,500 MW): total peaks near 2,400 MW around hour 9 and has a smaller second peak near 1,800 MW at hour 24; trough about 1,200 MW near hour 17-18. Residential space heating is the largest layer.
- **Summer, 2040** (y up to 300+ MW): total about 100 MW at hour 3-4, rising to about 320 MW around hour 11-12, and a second hump of about 280 MW near hour 20. Only the two water heating layers (commercial water heating in light blue at the bottom, residential water heating in orange on top) are present; the space heating layers are absent.
- **Fall, 2040** (y up to 1,000 MW): peak about 870 MW around hour 9; secondary peak about 580 MW around hour 21; trough about 350 MW near hour 15-16.
- **Winter, 2040** (y up to 8,000 MW): total about 4,600 MW at hour 1, peaking near 6,500 MW around hour 8-9, then declining steadily to about 3,200 MW at hour 24. Commercial space heating (purple) is about 1,800-3,300 MW and residential space heating (dark blue) is the next layer, with water heating thin.

Values read from the rendered charts are approximate.

[→ See original PDF page 17 for visual rendering]

[PDF p. 18 | printed p. 18]

# Typical Seasonal Load Shapes

_New England in Forecast Year 2040 by Load Zone_

> - Hourly county-level HP forecasts are aggregated to load zones

[DIAGRAM DESCRIPTION: Load zone map and seasonal HP load shapes by load zone]

At left, inside the callout box, a map of New England (axes: Latitude 42°N-46°N, Longitude 74°W-68°W; scale bar 100 km / 50 mi; basemap credit Esri, HERE, Garmin, USGS, EPA, NPS, NRCan) with counties outlined and colored by load zone: Connecticut (CT, southwest, salmon/blue-red), Rhode Island, Southeast Massachusetts (SEMA, purple), Northeast Massachusetts (NEMA, light blue), Western/Central Massachusetts (WCMA, orange), New Hampshire, Vermont, and Maine (large light-green area at the north and east). Color assignments are read from the rendered map and approximate.

At right, four stacked-area charts (2×2 grid) of New England HP demand in forecast year 2040: Spring, 2040 (y up to 2,500 MW); Summer, 2040 (y up to 300+ MW); Fall, 2040 (y up to 1,000 MW); Winter, 2040 (y up to 8,000 MW). X-axis: hour of day (1-24); y-axis: "Demand (MW)". Stack layers from bottom to top: WCMA (orange), NEMA (light blue), SEMA (purple), CT (dark blue), ME (yellow), NH (red), RI (green), VT (gray). The overall shape and magnitude of each season match the by-sector charts on slide 17; each load zone follows the same morning-peak profile, with WCMA, NEMA and CT among the larger layers in winter and spring.

[→ See original PDF page 18 for visual rendering]

[PDF p. 19 | printed p. 19]

# ENERGY AND PEAK DEMAND FORECAST

[PDF p. 20 | printed p. 20]

# Methodology for Calculating HP Energy

_Example: January, Forecast Year 2040_

- HP energy values derive from hourly demand as follows:

[DIAGRAM DESCRIPTION: Three-step method for calculating HP energy (example: January, forecast year 2040)]

Three bar charts joined by "Sum" and "=" arrows, each with a numbered caption box below.

1. **Sum the hourly demand of each day in each month of a weather year.** Bar chart titled by x-axis "Days in January", y-axis "Energy (GWh)" (0 to 250): 31 purple bars sorted in descending order, from about 212 GWh on the highest day down to about 40 GWh on the lowest, with most days between about 70 and 180 GWh. "Sum" arrow.
2. **Sum the daily energy in each month of each weather year.** Bar chart, x-axis "January by Weather Year (70 years)", y-axis "Energy (GWh)" (0 to 6,000): bars for individual weather years (the purple bar at left is about 3,050 GWh; others range from about 3,200 to about 5,200 GWh) and a green bar labeled "Mean" at about 4,250 GWh, with a dashed horizontal line at the mean. "=" arrow.
3. **Average the simulated energy across weather years to derive the monthly energy in a forecast year.** Bar chart of monthly energy, x-axis Jan-Dec, y-axis "Energy (GWh)" (0 to 4,500): Jan about 4,250 (green bar), Feb about 3,800, Mar about 2,950, Apr about 1,400, May-Sep about 400-430 each, Oct about 1,000, Nov about 2,000, Dec about 3,550.

Values read from the rendered charts are approximate.

[→ See original PDF page 20 for visual rendering]

[PDF p. 21 | printed p. 21]

# Calculating HP Demand Impacts on System Peak

_Example Winter Peak Day, 2038_

- The hourly forecast results in a dynamic interplay of modeled load components
  - Peak hour shifts due to the growth of one component affect the peak attribution of other components
  - Attribution of peak load values to components is path dependent
- A waterfall approach to the attribution of peak load contributions is used to standardize this forecast accounting
- Waterfall method steps (refer to plot):
  1. Base = Base peak load value: 19,339 MW
  2. EV = (Base+EV) – Base: 21,886 – 19,339 = 2,547 MW
  3. **HP = (Base+EV+HP) – (Base+EV): 32,315 – 21,886 = 10,429 MW**
  4. LargeLd = (Base+EV+HP+LargeLd) – (Base+EV+HP): 32,436 – 32,315 = 121 MW
  5. BTM PV = Gross – (Gross-BTM PV): 32,436 – 31,687 = 749 MW
  6. BTM BESS = (Gross-BTM PV) – Net: 31,687 – 31,556 = 121 MW

[DIAGRAM DESCRIPTION: Example winter peak day, 2038 — waterfall of load components]

Six small hourly (hour 1-24; y-axis MW, 0 to 40,000) stacked-area panels numbered 1-6, each with a red dot marking that panel's peak hour:

1. **Base**: Base load (blue) only, about 15,000-19,000 MW over the day, peak 19,339 MW near hour 19.
2. **Base + EV**: adds EV (green) on top; peak 21,886 MW near hour 19.
3. **Base + EV + HP**: adds HP (orange) on top; peak 32,315 MW around hour 8.
4. **Gross (Base + EV + HP + LgLd)**: adds large load (LgLd, purple); peak 32,436 MW.
5. **Gross – BTMPV**: adds BTM PV (light green, a midday hump of up to about 7,000 MW below the baseline); a red dotted line marks gross less BTM PV, peak 31,687 MW.
6. **Net (Gross – BTMPV – BESS)**: adds BESS (gray); a black dotted line marks net load, peak 31,556 MW.

Legend: Base Load (blue), EV (green), HP (orange), LgLd (purple), BTM PV (light green), BESS (gray), Net Load (black dotted line). The HP layer raises the system peak from the early evening (about hour 19) to the morning (about hour 8) in this example.

[→ See original PDF page 21 for visual rendering]

_Extractor note (not source text): The slide text prints "21,886 – 19,339 = 2,547 MW" for the EV step; the arithmetic matches. For the BTM PV step the slide prints "32,436 – 31,687 = 749 MW", also matching._

[PDF p. 22 | printed p. 22]

# 2026 HP Energy Forecast

_Monthly Energy by Load Zone_

[DIAGRAM DESCRIPTION: Monthly HP energy by load zone, 2026-2047, with regional gross energy share]

A monthly stacked-bar chart over 2026 to 2047 (x-axis, one tick per year). Left y-axis: "Energy (GWh)", 0 to about 4,200; right y-axis (orange): "Regional Gross Energy Share", 0% to 24%. Stack layers from bottom to top: WCMA (orange), NEMA (light blue), SEMA (purple), CT (dark blue), ME (yellow), NH (red), RI (green), VT (gray). A dashed orange line, "Regional Gross Energy Share", traces the monthly HP energy share of regional gross energy. Each year has a strong winter peak with very low summer months; the winter peaks grow each year from near zero in 2026 to about 4,200 GWh per month by 2046-2047 (about 24% of regional gross energy on the right axis). Intermediate winter peaks are roughly 500 GWh (2030), 1,000 GWh (2031), 2,000 GWh (2035), 2,800 GWh (2039-2040). Values read from the rendered chart are approximate.

[→ See original PDF page 22 for visual rendering]

[PDF p. 23 | printed p. 23]

# 2026 HP Summer Peak Demand Forecast

_Summer 50/50 Peak Demand by Load Zone_

**Summer Peak Demand (MW)**

| Year | CT | ME | NEMA | NH | RI | SEMA | VT | WCMA | ISONE |
| ---- | -- | -- | ---- | -- | -- | ---- | -- | ---- | ----- |
| 2026 | 0  | 0  | 0    | 0  | 0  | 0    | 0  | 0    | 2     |
| 2027 | 1  | 1  | 1    | 0  | 1  | 1    | 0  | 1    | 7     |
| 2028 | 2  | 2  | 2    | 1  | 1  | 2    | 1  | 2    | 13    |
| 2029 | 4  | 3  | 4    | 1  | 1  | 3    | 1  | 3    | 20    |
| 2030 | 5  | 4  | 5    | 2  | 2  | 5    | 1  | 5    | 29    |
| 2031 | 7  | 6  | 8    | 2  | 3  | 6    | 2  | 7    | 41    |
| 2032 | 9  | 8  | 10   | 3  | 4  | 9    | 3  | 9    | 55    |
| 2033 | 12 | 11 | 13   | 4  | 5  | 11   | 4  | 12   | 72    |
| 2034 | 15 | 14 | 17   | 5  | 6  | 15   | 5  | 15   | 92    |
| 2035 | 19 | 17 | 22   | 6  | 8  | 19   | 6  | 20   | 116   |

_Extractor note (not source text): the column order is CT, ME, NEMA, NH, RI, SEMA, VT, WCMA, ISONE, as printed (alphabetical load zones, not the CT, MA, ME... state order of slides 8-11)._

[DIAGRAM DESCRIPTION: Summer 50/50 HP peak demand by load zone, 2026-2046]

A stacked-bar chart. X-axis: year, 2026 to 2046 (ticks every 5 years, bars for each year). Y-axis: "Demand (MW)", 0 to 600. Stack layers from bottom to top: WCMA (orange), NEMA (light blue), SEMA (purple), CT (dark blue), ME (yellow), NH (red), RI (green), VT (gray). Total grows from about 2 MW in 2026 to about 540 MW in 2046, with the largest layers being WCMA, NEMA, SEMA and CT. Values read from the rendered chart are approximate.

[→ See original PDF page 23 for visual rendering]

[PDF p. 24 | printed p. 24]

# 2026 HP Winter Peak Demand Forecast

_Winter 50/50 Peak Demand by Load Zone_

**Winter Peak Demand (MW)**

| Year | CT  | ME    | NEMA | NH  | RI  | SEMA | VT  | WCMA | ISONE |
| ---- | --- | ----- | ---- | --- | --- | ---- | --- | ---- | ----- |
| 2026 | 35  | 49    | 40   | 15  | 11  | 31   | 18  | 41   | 241   |
| 2027 | 68  | 99    | 80   | 30  | 23  | 62   | 38  | 81   | 480   |
| 2028 | 110 | 159   | 131  | 50  | 37  | 101  | 63  | 132  | 783   |
| 2029 | 161 | 233   | 191  | 75  | 54  | 149  | 96  | 194  | 1,152 |
| 2030 | 224 | 322   | 264  | 106 | 75  | 206  | 134 | 268  | 1,600 |
| 2031 | 308 | 425   | 355  | 141 | 103 | 276  | 180 | 360  | 2,149 |
| 2032 | 411 | 555   | 465  | 184 | 139 | 362  | 237 | 471  | 2,823 |
| 2033 | 540 | 701   | 600  | 235 | 185 | 465  | 303 | 603  | 3,631 |
| 2034 | 699 | 864   | 747  | 298 | 235 | 576  | 382 | 748  | 4,550 |
| 2035 | 874 | 1,037 | 902  | 373 | 290 | 695  | 463 | 899  | 5,533 |

[DIAGRAM DESCRIPTION: Winter 50/50 HP peak demand by load zone, 2026-2046]

A stacked-bar chart. X-axis: year, 2026 to 2046 (ticks every 5 years, bars for each year). Y-axis: "Demand (MW)", 0 to 14,000. Stack layers from bottom to top: WCMA (orange), NEMA (light blue), SEMA (purple), CT (dark blue), ME (yellow), NH (red), RI (green), VT (gray). Total grows from about 240 MW in 2026 to about 12,700 MW in 2046. WCMA is about 1,900 MW and CT about 1,800 MW of the 2046 total. Values read from the rendered chart are approximate.

[→ See original PDF page 24 for visual rendering]

[PDF p. 25 | printed p. 25]

# Seasonal Peak Demand and Annual Energy

_New England CELT 2025 and CELT 2026 Comparison_

[DIAGRAM DESCRIPTION: CELT 2025 vs. CELT 2026 — ISONE HP annual energy, summer 50/50 peak, winter 50/50 peak]

Three line charts (x-axis: year, 2026 to 2046, with a marker each year), each comparing **CELT 2026** (blue line, circle markers) with **CELT 2025** (orange line, circle markers). The CELT 2026 line is lower than CELT 2025 in all three charts.

- **ISONE Annual HP Energy** (y: "Energy (GWh)", 0 to 25,000): CELT 2026 rises from about 250 GWh in 2026 to about 19,500 GWh in 2046; CELT 2025 rises from about 1,200 GWh to about 23,500 GWh.
- **ISONE HP Summer 50/50** (y: "Demand (MW)", 0 to 600): CELT 2026 rises from about 2 MW to about 540 MW in 2046; CELT 2025 from about 7 MW to about 575 MW. The two lines are close together until about 2036.
- **ISONE HP Winter 50/50** (y: "Demand (MW)", 0 to 16,000): CELT 2026 rises from about 240 MW to about 12,700 MW in 2046; CELT 2025 from about 450 MW to about 15,300 MW. The lines are nearly the same from about 2033 to 2036 (CELT 2026 slightly lower, with CELT 2025 crossing slightly above afterward) and diverge after about 2037.

Values read from the rendered charts are approximate.

[→ See original PDF page 25 for visual rendering]

[PDF p. 26 | printed p. 26]

# Seasonal Peak Demand

_New England 50/50 and 90/10 Comparison_

[DIAGRAM DESCRIPTION: ISONE HP summer and winter peak forecasts, 50/50 vs. 90/10]

Two line charts (x-axis: year, 2026 to 2046), each comparing the **50/50** forecast (light green line) with the **90/10** forecast (dark green line).

- **ISONE HP Summer Peak Forecast** (y: "Demand (MW)", 0 to 600): the two lines are almost identical, rising from about 2-5 MW in 2026 to about 540 MW (50/50) and about 548 MW (90/10) in 2046.
- **ISONE HP Winter Peak Forecast** (y: "Demand (MW)", 0 to 18,000): the 90/10 line sits well above the 50/50 line from the start and the gap widens: 50/50 rises from about 240 MW to about 12,700 MW in 2046, while 90/10 rises from about 350 MW to about 17,000 MW in 2046.

Values read from the rendered charts are approximate.

[→ See original PDF page 26 for visual rendering]
