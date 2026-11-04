# CMP Seasonal Heat Pump (SHP) Rate — Complete Rate Schedule

**Status:** Cancelled effective February 1, 2026 (Docket No. 2022-00152)
**Pilot Period:** January 1, 2023 – December 31, 2025
**Enrollment Cap:** 5,000 customers (reached ~3,134 at peak in Dec 2024)
**Eligibility:** Residential customers with air source heat pumps
**Reinstatement:** CMP filed Docket 2026-00248 requesting reinstatement; under MPUC review as of Oct 2026

## Rate Design Structure

The SHP rate was a **delivery-only** rate (supply/Standard Offer charges were the same as for all residential customers). It restructured delivery charges seasonally:

- **Winter (November–April):** Very low volumetric delivery rate (near zero at launch, rising over time)
- **Summer (May–October):** Very high volumetric delivery rate (concentrating annual delivery recovery into summer)
- **Fixed charge:** Higher than Rate A (no first-50-kWh inclusion)
- **Sales tax exemption:** First 750 kWh per month was sales-tax free

## Complete Rate History (from CMP Rate Bulletin A-SEASONAL)

**Source:** CMP Rate Bulletin A-SEASONAL, downloaded from https://www.cmpco.com/w/historical-pricing (Excel). File: `a-seasonal.xlsx` in this directory.

| Revision | Effective Date | Service Charge ($/mo) | Summer $/kWh (May–Oct) | Winter $/kWh (Nov–Apr) |
| -------- | -------------- | --------------------- | ---------------------- | ---------------------- |
| Original | Jan 1, 2023    | $31.67                | $0.158188              | $0.004064              |
| 1st Rev  | Jul 1, 2023    | $37.71                | $0.143196              | $0.004317              |
| 2nd Rev  | Jan 1, 2024    | $37.71                | $0.137508              | $0.004317              |
| 3rd Rev  | Jul 1, 2024    | $40.21                | $0.201362              | $0.012294              |
| 4th Rev  | Aug 1, 2024    | $40.67                | $0.200486              | $0.011418              |
| 5th Rev  | Jan 1, 2025    | $40.67                | $0.254547              | $0.011418              |
| 6th Rev  | Jul 1, 2025    | $40.55                | $0.278592              | $0.011226              |
| 7th Rev  | Oct 1, 2025    | $41.24                | $0.275610              | $0.008244              |

### Notable trends:

- **Service charge** rose 30% from $31.67 to $41.24 over the pilot period
- **Summer rate** rose 74% from $0.158 to $0.276 (driven by rising transmission and distribution costs loaded entirely on summer)
- **Winter rate** rose from $0.004 to ~$0.011 (peaking at $0.012 in Jul 2024) then fell back to $0.008
- The summer/winter ratio narrowed from 39:1 (launch) to 33:1 (final)

## Cross-Verification of Launch Rates

### From Tesla Motors Club, IRWG presentation, and Zondits blog:

- Tesla Motors Club, "Maine Electricity Tariffs" thread — https://teslamotorsclub.com/tmc/threads/maine-electricity-tariffs-cmp-a-tou-opts-a-tou-and-a-lm.282998/page-2
- MA IRWG NECPUC presentation (June 2024) — https://necpuc.org/wp-content/uploads/2024/06/MA-IRWG-NECPUC-6.21.24.pdf
- Zondits blog — https://www.zondits.com/seasonal-heat-pump-rate/

All three independently confirm the Jan 2023 launch values: $31.67/mo, $0.004064 winter, $0.158188 summer.

### Cross-verified with Portland Press Herald bill examples (Dec 18, 2022):

| Scenario | Summer kWh/mo | Winter kWh/mo | Annual SHP Bill |
| -------- | ------------- | ------------- | --------------- |
| 1        | 550           | 1,000         | $926            |
| 2        | 550           | 1,500         | $938            |
| 3        | 550           | 2,000         | $950            |

Back-calculation yields winter = $0.004/kWh and summer = $0.15817/kWh, matching exactly.

### From Demand Side Analytics report (Attachment 6 of CMP Final Report, Docket 2022-00152 Item 322):

Table 3 of that report shows the rates as of the 6th revision (Jul 1, 2025):

- Rate A: $26.60/mo, $0.108980/kWh all months
- SHP: $40.55/mo, $0.011226/kWh winter, $0.278592/kWh summer

## Rate A vs. SHP Comparison at Key Points in Time

### At launch (January 1, 2023):

| Component        | Rate A    | SHP Winter         | SHP Summer         |
| ---------------- | --------- | ------------------ | ------------------ |
| Service charge   | $13.66/mo | $31.67/mo          | $31.67/mo          |
| First kWh incl.  | 50 kWh    | 0 kWh              | 0 kWh              |
| Delivery per kWh | $0.086420 | $0.004064          | $0.158188          |
| Diff. vs. Rate A | —         | **-8.24 ¢** (-95%) | **+7.18 ¢** (+83%) |

### At final revision (October 1, 2025):

| Component        | Rate A (Oct 2025) | SHP Winter (Oct 2025) | SHP Summer (Oct 2025) |
| ---------------- | ----------------- | --------------------- | --------------------- |
| Service charge   | $29.88/mo         | $41.24/mo             | $41.24/mo             |
| First kWh incl.  | 50 kWh            | 0 kWh                 | 0 kWh                 |
| Delivery per kWh | $0.131239         | $0.008244             | $0.275610             |
| Diff. vs. Rate A | —                 | **-12.30 ¢** (-94%)   | **+14.44 ¢** (+110%)  |

### Transmission Component (from CMP Section 44.1):

- **A-SEASONAL transmission:** $0.110929/kWh, **May to October only** ($0.00 in winter)
- **Rate A transmission:** $0.047973/kWh year-round (Jan 2025 Section 44 values)
- The zero winter transmission accounts for ~$0.048 of the winter discount
- The doubled summer transmission ($0.111 vs. $0.048) accounts for ~$0.063 of the summer increase

## Demand Side Analytics Evaluation Key Finding

From CMP's Final Report (Docket 2022-00152, Item 322, Dec 5, 2025):

> "Following rate transition, we found that SHP accounts increased their electric consumption by about 1.4% (114 kWh) during the heating season (p-value = 0.01). The cooling season impact was also positive (1.1% or 44 kWh) but not statistically significant."

> "Accounts that moved from Rate A to the SHP rate paid about $100 more (or 8% more), on average, in their first year on the SHP rate relative to a baseline scenario where they did not change rates."

In other words: **the SHP rate did not meaningfully change customer behavior, and early enrollees actually paid more on average** (though this reversed in later rate revisions).

Stakeholders had mixed reactions:

> "As indicated in the analyses... neither alternative rate is meaningfully influencing customer usage. Stakeholders discussed whether enrollment in the alternative rates should necessarily result in a change in usage behavior, or whether customers whose usage naturally aligns with the incentives provided by the rates should enjoy those incentives regardless of a measurable change in behavior."

## Key Design Differences vs. Massachusetts HP Rates

Per the CT HP Rates expert testimony:

1. **Summer rate increase:** The SHP rate raised summer volumetric charges up to 14–17 ¢/kWh above the default. Massachusetts HP rates did **not** raise summer rates, guaranteeing savings for every enrollee.
2. **No guarantee of savings:** Because the SHP rate raised both the fixed charge and summer rates, customers with significant summer cooling usage could pay MORE than on Rate A.
3. **Revenue structure:** The SHP rate was designed to be approximately revenue-neutral for an average heat pump customer, but shifts revenue between seasons. Massachusetts designed its rates to simply discount winter delivery without any offsetting increase.

## Sources

1. **CMP Rate Bulletin A-SEASONAL** (Excel) — https://www.cmpco.com/w/historical-pricing → "A-SEASONAL" row. File: `a-seasonal.xlsx`
2. **CMP Final Report, Docket 2022-00152 Item 322** (Dec 5, 2025) — https://mpuc-cms.maine.gov/CQM.Public.WebUI/Common/CaseMaster.aspx?CaseNumber=2022-00152. Extracted: `cmp_final_report_2025_2022-152.md`
3. CMP Rate A Tariff — https://www.cmpco.com/documents/d/cmp/a
4. CMP Section 44 Transmission — https://www.cmpco.com/documents/40117/115962335/sect44.pdf
5. CMP Pricing Page — https://www.cmpco.com/account/understandyourbill/pricing
6. MPUC Residential Rates — https://www.maine.gov/mpuc/regulated-utilities/electricity/delivery-rates
7. Portland Press Herald, "Have a heat pump? New electric rates could save you money," Dec 18, 2022 — https://www.centralmaine.com/2022/12/18/new-electricity-delivery-rates-promise-to-save-money-for-mainers-who-read-the-fine-print/
8. Green & Healthy Maine HOMES, "CMP offers lower rates to encourage electrification," Spring 2023 — https://greenmainehomes.com/blog/central-maine-power-lower-rates-encourage-electrification
9. Competitive Energy Services, "An Update from a (Mostly) Electrified Home" — https://www.competitive-energy.com/blog/an-update-from-a-mostly-electrified-home
10. NEWS CENTER Maine, "Central Maine Power wants the state to approve two special rate plans," Oct 5, 2026 — https://www.newscentermaine.com/article/money/consumer/central-maine-power-wants-the-state-to-approve-two-special-rate-plans-for-high-electricity-users-but-green-energy-groups-say-other-options-are-better/97-723f3bf0-7197-4016-9e44-a108c57daacd
11. MPUC Docket 2026-00248 (SHP reinstatement request) — https://mpuc-cms.maine.gov/CQM.Public.WebUI/Common/CaseMaster.aspx?CaseNumber=2026-00248
12. Tesla Motors Club, "Maine Electricity Tariffs" thread — https://teslamotorsclub.com/tmc/threads/maine-electricity-tariffs-cmp-a-tou-opts-a-tou-and-a-lm.282998/page-2
13. MA IRWG NECPUC presentation (June 2024) — https://necpuc.org/wp-content/uploads/2024/06/MA-IRWG-NECPUC-6.21.24.pdf
14. Zondits, "A Seasonal Heat Pump Rate Can Incentivize Heat Pumps AND Solar Energy" — https://www.zondits.com/seasonal-heat-pump-rate/
