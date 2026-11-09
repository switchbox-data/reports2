---
source_file: "Synapse - 2024 - Avoided Energy Supply Components in New England 2024 Repor.pdf"
citekey: synapse_AvoidedEnergySupply_2024
zotero_item: "4HZWP4NM"
public_url: "https://drive.google.com/file/d/154NYJ1K_xbqwFq1uQeN2rifByQDQrYj0/view"
short_url: "https://pub.switch.box/synapse_AvoidedEnergySupply_2024"
source_url: "https://www.synapse-energy.com/sites/default/files/inline-images/AESC%202024%20May%202024.pdf"
md5: "4fb83ebfe927b541ac86cbf599b380be"
document_type: report
filer: Synapse Energy Economics, Sustainable Energy Advantage, North Side Energy, Resource Insight, Les Deman Consulting
pages_total: 436
extraction_scope: "partial: PDF pp. 122-150 (printed pp. 104-132), Chapter 4 Common Electric Assumptions, sections 4.4-4.8 (starts partway down PDF p. 122, at the heading 4.4) to the end of Chapter 4; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Second half of Chapter 4 (Common Electric Assumptions): renewable capacity factors and offshore wind interconnection, expected nuclear/coal/gas/oil/battery additions and retirements, intra- and inter-regional transmission and imports, operating-unit characteristics, and the emissions regulations embedded in the electric price forecast (RGGI, Massachusetts 310 CMR 7.74/7.75, state GHG targets and Massachusetts sector sublimits, EPA's proposed section 111 rule, IRA/BIL)."
why_here: "Shows how the AESC production-cost model (EnCompass) treats generation additions and retirements, transmission, RGGI and Massachusetts GHG compliance costs, which shape the marginal energy and capacity costs Switchbox uses as a benchmark for marginal cost of service in New England rate cases."
---

_Extractor note (not source text): this file holds PDF pp. 122-150 (printed pp. 104-132) of AESC 2024, Chapter 4: Common Electric Assumptions, §§4.4-4.8 (to the end of the chapter); the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, with no corrections to the source's typographical errors (a few are flagged `[sic]`). Hyperlink targets are taken from the PDF's link annotations; where an annotation target has no scheme (footnote 151), `https://` has been added to make the link work. Italics follow the source's font styling._

[PDF pp. 1-121 not transcribed: front matter, Chapters 1-3 and §§4.1-4.3 of Chapter 4 (§§4.1-4.3 are in `04a_common_electric_assumptions_4-1_to_4-3.md` of this folder; the earlier chapters are in the other files of this folder, see README.md)]

# 4. Common Electric Assumptions (continued: §§4.4-4.8)

[PDF p. 122 | printed p. 104]

_Extractor note (not source text): the part of this page before §4.4 (the end of §4.3, from "to set the installed-capacity requirement for FCA 18" through "see Chapter 5: Avoided Capacity Costs.") is in `04a_common_electric_assumptions_4-1_to_4-3.md`; this file starts at the heading "4.4. Renewable energy assumptions"._

## 4.4. Renewable energy assumptions

This section contains additional information on renewable energy capacity factors and offshore wind interconnections. Most other assumptions relating to renewable energy are described in Chapter 7. _Avoided Cost of Compliance with Renewable Portfolio Standards and Related Clean Energy Policies._

### Renewable energy capacity factors

We used data from ISO New England's 2022 New England Variable Energy Data series to create renewable dispatch shapes.[^140] This dataset includes modeled hourly historical wind and solar generation for 2000 to 2021. For our core energy modeling, we used the renewable dispatch data from 2002 to be consistent with our load shape weather year. We then scaled these 2002 dispatch shapes to match the annual capacity factors used in SEA's REMO model to ensure our annual renewable energy generation was consistent with the REMO assumptions. For the stochastic capacity modeling (described below in Chapter 5: _Avoided Capacity Costs_), we used the same ISO New England dataset to create similar dispatch shapes for 2000 to 2021.

### Offshore wind interconnection

The REMO Model provides information on projected offshore wind capacity and generation but does not specify where these facilities interconnect with New England's electric grid. For southern New England, we assume that offshore wind built in southern New England is built in the U.S. Bureau of Ocean Energy Management's designated lease zones (see Figure 27). We note there is ongoing discussion on where these offshore wind facilities will interconnect, including an ongoing multistate effort to comprehensively plan for these new resources.[^141] Options for interconnection include locations on or near Cape Cod; New London, Montville, or Bridgeport, CT; Quonset, RI; Brayton Point, MA; or in the Greater Boston region. In order to minimize price anomalies, we distribute the offshore wind interconnection points throughout southern New England. Although there is uncertainty about which interconnection points will be used, to what degree, and when, we rely on a simplified "cycling"

[^140]: See ISO New England. _2022 ISO-NE Variable Energy Resource (VER) Data Series (2000-2021) Rev. 0_. May 11, 2022. available at [https://www.iso-ne.com/static-assets/documents/2022/05/2022_isone_ver_dataset_2000_2021_rev0.zip](https://www.iso-ne.com/static-assets/documents/2022/05/2022_isone_ver_dataset_2000_2021_rev0.zip).

[^141]: See "New England Energy Vision" materials, available at [https://newenglandenergyvision.com/](https://newenglandenergyvision.com/).

[PDF p. 123 | printed p. 105]

methodology to allocate the offshore wind throughout various modeling zones. Using 1200-MW blocks, we change the interconnection point of offshore wind projects as they are built, moving from Phase I, to Phase 2, to Phase 3 (as described in Figure 27), and repeating this cycle as necessary. This results in offshore wind becoming roughly evenly distributed across four different EnCompass modeling zones.

We apply a similar approach to offshore wind being deployed in southeastern Maine. Less information is currently available on points of interconnection for offshore wind projects likely to be deployed in the Gulf of Maine. Based on information in a July 2023 NREL study, we assume these projects are interconnected at points in Southeastern Maine (e.g., Yarmouth), New Hampshire (e.g., Seabrook), and metro Boston (e.g., Cape Ann or Boston itself). This results in offshore wind becoming roughly evenly distributed across three different EnCompass modeling zones. We note that in all counterfactuals, substantial quantities of offshore wind are not built in Maine until the late 2030s, minimizing the impact these assumptions have on near-term avoided costs.

We note that because the offshore wind costs being modeled include an average, incremental transmission cost (as opposed to a location-specific transmission cost, or a transmission cost based on a strategic regional approach to interconnection), our "cycling" approach may overestimate the cost of some offshore wind projects and underestimate the costs for other projects.

[PDF p. 124 | printed p. 106]

**Figure 27. Bureau of Ocean Energy Management lease zones in southern New England and potential interconnection points**

[DIAGRAM DESCRIPTION: Figure 27. Bureau of Ocean Energy Management lease zones in southern New England and potential interconnection points]

A slide-style map (a copy of slide 4 of the New England Energy Vision "New England States' Transmissions RFI Technical Session") of the southern New England coast and offshore waters (Massachusetts Bay and Cape Cod Bay to the north and east, Rhode Island Sound and Nantucket Shoals to the south and east), titled "Phased Offshore Wind Transmission Concept Plan". Three coloured legend lines at the top read: "Phase I two 1200 MW HVDC lines in Blue one each for MA and CT" (blue text), "Phase II Future 1200 MW HVDC lines in Red" (red text) and "NYSERDA Beacon 1230 MW HVDC line in Green (to Astoria, Queens)" (green text). On the map, thick blue, red and green lines run from a cluster of offshore lease areas south of Rhode Island/Martha's Vineyard to shore at the labeled landing points, with small diamond markers and dashed/double-arrow lines among the converters in the lease-area cluster. Callout boxes (each with a circle on the map) label the interconnection points and their capacities: "Mystic (MA): 1,200 MW" (Boston Harbor area; reached by a red line running up the east side of Cape Cod), "Brayton Point (MA): 1,600 MW", "Kent County/ Davisville (RI): 1,000 MW", "Cape Cod (Bourne/ Barnstable) (MA): 2,400 MW", and "Montville (CT): 800 MW"; a separate note at the left edge reads "To Bridge port" (Bridgeport, CT), where blue, red and green lines head west along the Connecticut shore. A legend in the lower left lists six lease areas by colour: Deepwater Wind/Orsted Lease Areas (OCS-A 0486, 0487); Bay State Wind Lease Area (OCS-A 0500); Vineyard Wind Lease Area (OCS-A 0501); Equinor Wind Lease Area (OCS-A 0520); Mayflower Wind Energy Lease Area (OCS-A 0521); Vineyard Wind Lease Area (OCS-A 0522). A text box at the bottom of the figure states: "Dashed lines represent future potential interconnections between converters to increase offshore grid flexibility" and "Double Arrow lines represent future potential interconnections between converters of projects in different ISOs to permit controlled interregional transfers of offshore wind power". The figure shows where offshore wind built in the southern New England lease zones could interconnect (the points used in the "cycling" approach described above).

[→ See original PDF page 124 for visual rendering]

_Source: New England Energy Vision. 2022. "New England States' Transmissions RFI Technical Session," slide 4. <https://newenglandenergyvision.files.wordpress.com/2022/10/state-of-ct_-tech-mtg-slides.pdf>._

[PDF p. 125 | printed p. 107]

## 4.5. Anticipated non-renewable resource additions and retirements

The following section highlights key input assumptions regarding retirements of existing units as well as anticipated additions of new generating units. This section is not meant to be a comprehensive census of all existing generators; instead, it is meant to provide an overview of the significant changes to non-renewable capacity expected to occur during the analysis period.[^142]

Note that plant additions and retirements may be affected by federal policies, including the IRA and U.S. EPA's proposed regulations under Section 111 of the _Clean Air Act_. For more on these expected impacts, see below text (where relevant) and Section 4.8: _Embedded emissions regulations_.

In addition, all existing resources will be eligible to endogenously retire starting on June 1, 2028, the start of the FCA-18 commitment period.

### Nuclear units

There are two remaining nuclear plants in New England: Seabrook (located in New Hampshire) and Millstone (located in Connecticut). Seabrook has one unit, and Millstone has two (see Table 44). None of the three units have announced a retirement date. In the recent past, the Nuclear Regulatory Commission (NRC) relicensed Pilgrim 1 (previously located in Massachusetts and retired in May 2019), Millstone 2, and Millstone 3—along with many other reactors outside New England—without denying a single extension.[^143] Furthermore, we note that the IRA includes zero-emission production tax credits for nuclear plants. Although this financial support expires in 2032 under the current text of the IRA, it is indicative of the broad federal support for existing nuclear plants in the United States. Based on this track record and the lack of evidence suggesting that the NRC would deny license renewals for any of these plants, we assume that all three nuclear units continue to operate throughout the entire modeling period.[^144]

**Table 44. Nuclear unit detail**

| Unit        | State | Capacity (MW) | Announced Retirement Date | Current License Expiration Date | Assumed operational through Dec 2050? |
| ----------- | ----- | ------------: | ------------------------- | ------------------------------- | ------------------------------------- |
| Seabrook 1  | NH    |       1,242.0 | None                      | March 2050                      | Yes                                   |
| Millstone 2 | CT    |         909.9 | None                      | July 2035                       | Yes                                   |
| Millstone 3 | CT    |       1,253.0 | None                      | November 2045                   | Yes                                   |

[^142]: Note that we are not proposing to include any incremental demand response resources in our analysis, in line with our assumptions for conventional energy efficiency resources.

[^143]: NEI. "Nuclear Energy in the U.S." _Nei.org_. Available at [https://www.nei.org/resources/statistics](https://www.nei.org/resources/statistics).

[^144]: These assumptions are consistent with those assumed by ISO New England in its 2019 Regional System Plan (see [https://www.iso-ne.com/static-assets/documents/2019/10/rsp19_final.docx](https://www.iso-ne.com/static-assets/documents/2019/10/rsp19_final.docx), page 152), with the addition of an assumed license extension for Seabrook 1. These assumptions do not appear to have been modified in more recent editions of the Regional System Plan (see [https://www.iso-ne.com/system-planning/system-plans-studies/rsp](https://www.iso-ne.com/system-planning/system-plans-studies/rsp)).

[PDF p. 126 | printed p. 108]

We do not model any incremental nuclear unit additions during the study period.

### Coal units

As of September 2023, there are two coal units operating in New England, both located at the Merrimack power plant (see Table 45). Other recently retired plants include Bridgeport Station 3 (retired June 2021), Brayton Point (retired June 2017), Mount Tom (retired June 2014), Salem Harbor (retired June 2014), and Schiller (retired July 2020).

The Merrimack power plant consists of two coal-fired units, and two 19-MW gas-fired combustion turbines. The two coal units at Merrimack were built in 1960 and 1968. Both Merrimack coal units feature a wet fluidized gas desulphurization (FGD) system to control for sulfur dioxide (SO₂), a selective catalytic reduction (SCR) system to control for nitrogen oxide (NOₓ), and an electrostatic precipitator (ESP) to control for particulate matter. In 2021, Merrimack's two coal units operated with an aggregate capacity factor of 7 percent. All four Merrimack units have capacity commitments through FCA-16 (i.e., through May 31, 2026), but not in FCA-17. Given this change in obligation, we assume that both Merrimack 1 and 2 retire on May 31, 2026, while the other two (gas-fired) Merrimack units continue to be operational throughout the analysis period.

**Table 45. Coal unit detail**

| Unit        | State | Capacity (MW) | Announced Retirement Date | Modeled Retirement Date |
| ----------- | ----- | ------------: | ------------------------- | ----------------------- |
| Merrimack 1 | NH    |         113.6 | None                      | May 2026                |
| Merrimack 2 | NH    |         345.6 | None                      | May 2026                |

We do not model any incremental coal unit additions during the study period.

### Natural gas and oil units

Throughout the study period, we assume over 77 MW of new capacity additions from natural gas or oil resources. Table 46 lists the units added exogenously during the study period. Data on capacities and online dates are from EIA's Form 860 and the FCM. These resources are assumed to be primarily natural-gas-fired.

**Table 46. Incremental natural gas and oil additions**

| Unit                             | State | Capacity (MW) | Modeled Online Date | Unit Type          |
| -------------------------------- | ----- | ------------: | ------------------- | ------------------ |
| Hartford Hospital Cogeneration 5 | CT    |           5.5 | Jan 2026            | Combined Cycle     |
| Hartford Hospital Cogeneration 6 | CT    |           5.5 | Jun 2026            | Combustion Turbine |
| MMWEC Simple Cycle Gas Turbine   | MA    |            65 | Jun 2023            | Combustion Turbine |

[PDF p. 127 | printed p. 109]

In addition, there are a number of major natural gas- and oil-fired units which are assumed to retire during the study period (see Table 47). Unit retirements are based on announcements by the unit owners. We do not assume any additional exogenous natural gas- or oil-fired unit retirements beyond those detailed in this table.

**Table 47. Major natural gas and oil retirements**

| Unit                                | State | Capacity (MW) | Announced / Modeled Retirement Date | Unit Type          | Notes                             |
| ----------------------------------- | ----- | ------------: | ----------------------------------- | ------------------ | --------------------------------- |
| Mystic Generating Station GT81      | MA    |         278.6 | June 2024                           | Combined Cycle     | -                                 |
| Mystic Generating Station GT82      | MA    |         278.6 | June 2024                           | Combined Cycle     | -                                 |
| Mystic Generating Station GT93      | MA    |         278.6 | June 2024                           | Combined Cycle     | -                                 |
| Mystic Generating Station GT94      | MA    |         278.6 | June 2024                           | Combined Cycle     | -                                 |
| Mystic Generating Station ST85      | MA    |         315.0 | June 2024                           | Combined Cycle     | -                                 |
| Mystic Generating Station ST96      | MA    |         315.0 | June 2024                           | Combined Cycle     | -                                 |
| Cape Gas Turbine GT4                | MA    |          17.5 | May 2026                            | Combustion Turbine | FCA16 Obligation through May 2026 |
| Cape Gas Turbine GT5                | MA    |          17.5 | May 2026                            | Combustion Turbine | FCA16 oblig through May 2026      |
| William F Wyman Hybrid (Yarmouth) 3 | ME    |         113.6 | May 2027                            | Steam Turbine      | FCA17 oblig. Through May 2027     |
| William F Wyman Hybrid (Yarmouth) 4 | ME    |         632.4 | May 2027                            | Steam Turbine      | FCA17 oblig. Through May 2027     |
| Middletown 2                        | CT    |         113.6 | May 2027                            | Steam Turbine      | FCA oblig. through May 2027       |
| Middletown 4                        | CT    |         414.9 | May 2027                            | Steam Turbine      | FCA oblig. through May 2027       |
| Middletown 10                       | CT    |          18.5 | June 2023                           | Steam Turbine      | No FCA oblig. in Jun 2023         |
| Maine Independence Station GEN1     | ME    |         177.8 | June 2023                           | Combined Cycle     | No FCA oblig. in Jun 2023         |
| Maine Independence Station GEN2     | ME    |         177.8 | June 2023                           | Combined Cycle     | No FCA oblig. in Jun 2023         |
| Maine Independence Station GEN3     | ME    |         194.6 | June 2023                           | Combined Cycle     | No FCA oblig. in Jun 2023         |
| Norden #2                           | CT    |             2 | May 2026                            | Steam Turbine      | FCA16 oblig through May 2026      |
| Norden #3                           | CT    |             2 | May 2026                            | Steam Turbine      | FCA16 oblig through May 2026      |

[PDF p. 128 | printed p. 110]

### Large-scale battery storage resources

Table 48 identifies the battery storage resources assumed to be added during the study period. This list includes over 730 MW of new battery storage. These resources are in addition to the BTM storage resources described above in Section 4.3: _New England system demand and energy components_. Data on capacities and online dates are from EIA's Form 860 and the resources with obligations in the forward capacity market.

**Table 48. New battery storage additions**

| Unit                             | State | Capacity (MW) | Modeled Online Date | Unit Type | Source  |
| -------------------------------- | ----- | ------------: | ------------------- | --------- | ------- |
| Outer Cape Community Battery     | MA    |            25 | Dec 2022            | Battery   | EIA 860 |
| Syncarpha Hybrid CSGs*           | MA    |             9 | 2021, 2022**        | Battery   | EIA 860 |
| AES Distributed Energy Projects* | MA    |          35.8 | 2021,2022**         | Battery   | EIA 860 |
| Ocean State BTM                  | RI    |             3 | Jun 2022            | Battery   | EIA 860 |
| Other ISO-NE < 5 MW Projects*    | MA    |          90.2 | 2021, 2022          | Battery   | EIA 860 |
| Rumford ESS                      | ME    |           4.9 | Jun 2021            | Battery   | FCA     |
| Medway Grid, LLC                 | MA    |           250 | Jun 2026            | Battery   | FCA     |
| Cross Town Energy                | ME    |           175 | Jun 2026            | Battery   | FCA     |
| Cranberry Point Battery Storage  | MA    |           150 | Jun 2026            | Battery   | FCA     |
| Great Lakes Millinocket          | ME    |            20 | Jun 2026            | Battery   | FCA     |

_Extractor note (not source text): the asterisks in Table 48 (`*` on three unit names, `**` on two online dates) are printed in the table, but the PDF page prints no corresponding note text._

### Other resources

Note that our analysis also includes several other existing resources not discussed in the above sections. These include conventional hydroelectric resources, pumped-storage hydroelectric resources, and other natural-gas-fired and oil-fired resources that are not assumed to exogenously retire during the study period.

Other resources (e.g., biomass, wind) may have specific retirement dates.[^145] These retirements and additions are accounted for in Section 4.4: _Renewable energy_ .

[^145]: These retirements include Pinetree Power (MA) in June 2022.

[PDF p. 129 | printed p. 111]

### Generic non-renewable resource additions

In addition to known and anticipated capacity additions, we allow the EnCompass model to construct generic unit additions of the types represented in Table 49 if there is a peak demand need. EPA recently announced its proposed _Greenhouse Gas Standards and Guidelines for Fossil Fuel-Fired Power Plants,_ which is discussed in greater depth below in Section 4.8: _Embedded emissions regulations._ We assume all new fossil units will be compliant with this rule. As a result, some of the operational parameters (e.g., fuel blends and capacity factors caps) are significantly different compared to the 2021 AESC Study. Table 50 outlines the compliance options for new gas plants that we were modeled [sic], along with the retrofit costs and incremental operational costs associated with the given retrofits. The base costs (capex, fixed and variable O&M, and heat rates) are similar though. Note that there are two types of each generic gas addition: one type that is built in Massachusetts load zones (and therefore subject to Mass DEP 310 CMR 7.74) and one type that is built in any of the other New England load zones.[^146] Our analysis does not take permitting into account for these endogenous builds; resources are built purely according to least-cost economics of the electricity system.

**Table 49. Operational characteristics of generic conventional resources assumed in the EnCompass model**

|                                            | Unit           | Natural gas-fired combined cycle | Natural gas-fired combustion turbine | Battery Storage | Long-Duration Storage |
| ------------------------------------------ | -------------- | -------------------------------: | -----------------------------------: | --------------: | --------------------: |
| Maximum size                               | _MW_           |                              702 |                                  237 |              10 |                   100 |
| Minimum size                               | _MW_           |                              225 |                                  120 |               - |                     - |
| Heat rate                                  | _Btu/kWh_      |                            6,360 |                                9,720 |               - |                     - |
| Variable O&M costs                         | _2024 $/MWh_   |                            $2.13 |                                $7.27 |               - |                     - |
| Fixed O&M costs                            | _2024 $/kW-yr_ |                           $33.40 |                               $26.29 |             $40 |                   $18 |
| Unabated CO₂ emissions rate                | _lb/MMBtu_     |                              119 |                                  119 |               - |                     - |
| Duration                                   | _hours_        |                                - |                                    - |      4, 6 and 8 |                    50 |
| Round Trip Efficiency                      | _%_            |                                - |                                    - |             85% |                   50% |
| Capital costs (exclusive of any retrofits) | _2024 $/kW_    |                  $1,347 - $1,096 |                        $1,214 - $984 |   $2,695 - $934 |                $2,269 |

_Note: Each type of generic fossil resource may be fueled either with natural gas or fuel oil. Range of capital costs represents 2027-2050 cost trajectory and range of durations for battery storage._

_Source: NREL's 2023 ATB; "Clean, Reliable, Affordable: The Value of Multi-Day Storage in New England." Form Energy. September 2023. Available at <https://formenergy.com/wp-content/uploads/2023/09/Form-ISO-New-England-whitepaper-09.27.23.pdf>._

[^146]: More information on this environmental regulation can be found in the subsequent section on electricity commodities.

[PDF p. 130 | printed p. 112]

**Table 50. Compliance pathways and associated costs for new gas units under EPA's proposed _Greenhouse Gas Standards and Guidelines for Fossil Fuel-Fired Power Plants_**

_Extractor note (not source text): in the PDF the "System Contribution" cell spans the two rows beneath it (Peaker, Intermediate, Baseload); it is printed once per group here, with the continuation row's cell left blank. Cells printed as "none" are shown as printed._

| System Contribution | Resource Type      | Fuel Blend                                                                                                 | Capacity Factor Constraint | Carbon Capture and Sequestration (CCS)                           | Retrofit Cost _(2024 $/kW)_ | Incremental O&M costs _(2024 $)_ |
| ------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------- | -------------------------- | ---------------------------------------------------------------- | --------------------------- | -------------------------------- |
| Peaker              | Combined Cycle     | Only ever burns natural gas                                                                                | 20%                        | No                                                               | none                        | none                             |
|                     | Combustion Turbine | Only ever burns natural gas                                                                                | 20%                        | No                                                               | none                        | none                             |
| Intermediate        | Combined Cycle     | Natural gas through 2031, 30% hydrogen blend (by volume) in 2032 onward                                    | 50%                        | No                                                               | none                        | none                             |
|                     | Combustion Turbine | Natural gas through 2031, 30% hydrogen blend (by volume) in 2032 onward                                    | 50%                        | No                                                               | none                        | none                             |
| Baseload            | Combined Cycle     | Natural gas through 2031, 30% hydrogen blend (by volume) from 2032–2037, 96% hydrogen blend in 2038 onward | No limit                   | No                                                               | $304                        | none                             |
|                     | Combined Cycle     | Natural Gas                                                                                                | No limit                   | 90% CCS requirement starting in 2038. Parasitic load is modeled. | $1,240                      | FOM: $17/kW-yr; VOM: $19/MWh     |

_Note: Assumes 25% base capex to retrofit facility._

_Sources: Öberg, Simon, Mikael Odenberger, and Filip Johnsson. 2020. "Exploring the competitiveness of hydrogen-fueled gas turbines in future energy systems." International Journal of Hydrogen Energy; Capital Cost and Performance Characteristic Estimates for Utility Scale Electric Power Generating Technologies, Sargent and Lundy._

## 4.6. Transmission, imports, and exports

This section describes the existing, under construction, and planned intra-regional transmission modeled in the AESC 2024 study. It also describes our assumptions on new transmission between New England and other adjacent balancing authorities, and how we model imports over these inter-regional transmission lines in the analysis.

[PDF p. 131 | printed p. 113]

### Intra-regional transmission

The interface limits used in the AESC 2024 study reflect both the existing system and the ongoing transmission upgrades discussed in ISO New England's Regional System Plan.[^147] The transmission paths that link each of the 13 modeled regions in New England are based on transmission limits published by ISO New England (see Table 51).[^148]

**Table 51. Group transmission limits**

_Extractor note (not source text): in the PDF the "Transmission Limit" name and the A to B / B to A values each span all the path rows of their group; they are printed once per group here, with the continuation rows' cells left blank. Where the B to A cell is empty in the PDF (NE Southeast, NE SW CT) it is left empty._

| Transmission Limit | Path                                                | A to B (MW) | B to A (MW) |
| ------------------ | --------------------------------------------------- | ----------: | ----------: |
| NE East-West       | NE Massachusetts Central - NE Massachusetts West    |       3,500 |       3,000 |
|                    | NE New Hampshire - NE Vermont                       |             |             |
|                    | NE Rhode Island - NE Connecticut Northeast          |             |             |
| NE North-South     | NE New Hampshire - NE Boston                        |       2,725 |       2,725 |
|                    | NE New Hampshire - NE Massachusetts Central         |             |             |
|                    | NE Vermont - NE Massachusetts West                  |             |             |
|                    | Hydro Quebec - NE Massachusetts Central             |             |             |
| NE SEMA/RI         | NE Massachusetts Southeast - NE Boston              |       1,800 |       3,400 |
|                    | NE Rhode Island - NE Boston                         |             |             |
|                    | NE Rhode Island - NE Connecticut Northeast          |             |             |
|                    | NE Rhode Island - NE Massachusetts Central          |             |             |
| NE Southeast       | NE New Hampshire - NE Boston                        |       5,150 |             |
|                    | NE Massachusetts Central - NE Boston                |             |             |
|                    | NE Rhode Island - NE Connecticut Northeast          |             |             |
|                    | NE Rhode Island - NE Massachusetts Central          |             |             |
| NE SW CT           | NY K Long Island - NE Norwalk Stamford              |       2,800 |             |
|                    | NE Connecticut Northeast - NE Connecticut Southwest |             |             |
| NE Connecticut     | NE Connecticut Northeast - NY K Long Island         |       3,400 |       3,400 |
|                    | NY K Long Island - NE Norwalk Stamford              |             |             |
|                    | NE Massachusetts West - NE Connecticut Northeast    |             |             |
|                    | NE Rhode Island - NE Connecticut Northeast          |             |             |
|                    | NY G Hudson Valley - NE Connecticut Northeast       |             |             |

_Note: Internal transmission limits are based on ISO New England's published Transmission Transfer Zone Capabilities for FCA 18 in <https://www.iso-ne.com/static-assets/documents/2023/03/a08_fca_18_transmission_transfer_capability_and_capacity_zone_development.pptx>, slide 8._

[^147]: Regional System Plan documents can be found on ISO New England's website at [https://www.iso-ne.com/system-planning/system-plans-studies/rsp](https://www.iso-ne.com/system-planning/system-plans-studies/rsp).

[^148]: Note that recent analysis by ISO New England that examines large amounts of renewable construction has found that, depending on where and how much renewable capacity is built, at a certain point, additional transmission capacity is required to facilitate the movement of renewable generation in northern New England (i.e., areas with favorable wind capacity factors) to southern New England (i.e., areas of high customer load). In response to this, AESC 2024 models one new 1200 MW transmission line between Maine West Central and Massachusetts Central beginning in 2030. The transmission line is intended to help limit issues of curtailment in Maine. For more information, see ISO New England. _2050 Transmission Study Draft Report_. November 1, 2023. Available at [https://www.iso-ne.com/static-assets/documents/100005/2023_11_01_pac_2050_transmission_study_draft.docx](https://www.iso-ne.com/static-assets/documents/100005/2023_11_01_pac_2050_transmission_study_draft.docx).

[PDF p. 132 | printed p. 114]

### Inter-regional transmission

In addition, we model transmission between subregions of New England and adjacent balancing authorities in New York, Québec, and New Brunswick. As with intra-regional transmission, transmission lines between these regions are typically grouped into aggregate links with aggregate transfer capacities. We model and export quantities between New England and adjacent balancing areas on an hourly basis, with an 8760-shape based on averages of recent historical quantities. Synapse calibrated transfers on these lines such that transfers modeled in historical years resemble actual historical transfers.

In addition, we model an incremental 1,200 MW transmission line from Québec to southeast Maine, per the topology of the New England Clean Energy Connect (NECEC) project.[^149] This line is modeled as providing 9.45 TWh per year. This transmission line represents compliance with Massachusetts' 2017 _Act to Promote Energy Diversity_, and the associated long-term contracts signed per that legislation. Per the latest data available, we assume this line will instead be energized on January 1, 2027. Because this cost is assumed to be unavoidable to Massachusetts ratepayers, we do not develop or incorporate a price for this resource at this time. See Section 7.1: _Assumptions and methodology_ for more information about this assumption.

## 4.7. Operating unit characteristics

Under the production-cost modeling framework, EnCompass represents the detailed operations of individual generating units. This representation includes detail on following operational characteristics for dispatch data:

- Unit type (steam-cycle, combined-cycle, simple-cycle, cogeneration, etc.)
- Fuel type (including dual-fuel capabilities, startup fuel usage, and fuel delivery point or basin of origin)
- Heat rate values and curve
- Seasonal capacity ratings (maximum and minimum)
- Variable O&M costs
- Commitment bid adders and multipliers
- Forced outage rates and planned outage rates and schedules

[^149]: See the New England Clean Energy Connect website at [https://www.necleanenergyconnect.org/](https://www.necleanenergyconnect.org/) for more information. Our analysis does not currently make any assumptions regarding the construction of the proposed Twin States Energy Link project ([https://www.twinstatescleanenergylink.com/](https://www.twinstatescleanenergylink.com/)) or any other transmission projection conceived to increase connections between ISO New England and adjacent balancing authorities.

[PDF p. 133 | printed p. 115]

- Minimum up and down times, including maximum hours for warm and hot start scenarios
- Quick start, regulation, and spinning reserves capabilities
- Startup costs
- Ramp rates
- CO₂ emission rates
- Seasonal and/or hourly capacity factor profiles for hydro, wind, and solar resources
- Acceptable curtailment levels for hydro, wind, and solar resources
- Storage charge and discharge rates (in MW), maximum energy-stored levels (in MWh), and payback rates for pumped hydropower and battery storage

The model uses unit operational restraints (for example, minimum up times and ramp rates) to simulate unit commitment for hourly, chronological model runs. During unit operations, units incur costs based on fuel usage, variable O&M costs, and emission costs. Operational units also receive revenue based on their provision of grid services, including energy, regulation, and reserve services. Every model run produces an estimate of each unit's profitability given a dispatch pattern optimized to produce the lowest overall electric system costs for the region. O&M costs for existing conventional generation are based on unit-specific data contained in EnCompass.

## 4.8. Embedded emissions regulations

This section contains detail on the emission regulations embedded in the electric commodity forecast.

### The Regional Greenhouse Gas Initiative

All six New England states are founding members of RGGI. Under the current program design, the six states (along with New York, Maryland, Delaware, New Jersey, and Virginia) conduct four auctions each year in which CO₂ allowances are sold to emitters and other entities.

In August 2017, the RGGI states announced a set of proposed program changes for 2021 through 2030.[^150] Under this extended program design, the RGGI states are set to continue reducing CO₂ emissions through 2030, eventually achieving a CO₂ emissions level 30 percent below 2020 levels. This program design also put forth a number of changes to the "Cost Containment Reserve" (a mechanism that allows for the release of more allowances in an auction if the price exceeds a certain threshold) and the creation of an "Emissions Containment Reserve" (a mechanism which withholds a number of

[^150]: For more information on the proposed program review, see [https://www.rggi.org/program-overview-and-design/program-review](https://www.rggi.org/program-overview-and-design/program-review).

[PDF p. 134 | printed p. 116]

available allowances if the allowance price remains below a certain threshold). Together, these triggers effectively act as a floor and ceiling on RGGI prices.[^151][^152] The RGGI states are currently conducting a Third Program Review, which will likely set cost containment reserve (CCR) and emissions containment reserve (ECR) caps between 2031 and 2040 and may make other adjustments to the caps for 2026 to 2030.[^153]

In addition, the RGGI region has been expanding and changing in recent years. The first new state to join RGGI was New Jersey in January 2020 (rejoining the program after leaving it in 2012).[^154] Later in 2020, Virginia finalized its rulemaking to join RGGI, effective January 1, 2021.[^155] Then in June 2023, the Virginia Air Pollution Control Board voted to withdraw the state from RGGI at the end of the year, with environmental groups challenging the Board's authority to make this decision.[^156] Pennsylvania started the process of joining RGGI in 2019 and finalized its rulemaking in April 2022. However, Pennsylvania has yet to participate in any RGGI auctions, and its role in RGGI remains uncertain due to ongoing legal challenges.[^157]

Figure 28 displays the recent prices for RGGI allowances from auctions in 2010 through 2023. This figure also shows the prices associated with the ECR and CCR. Although two states (Maine and New Hampshire) do not use the ECR (the floor price), emissions from these two states make up a small fraction of RGGI-wide emissions and are unlikely to have a substantial effect on the price. Prices lower than the ECR are possible in situations where the full ECR (e.g., 10 percent of the allowances sold in any given auction) is withheld and there is still not enough demand at the trigger price for the remaining allowances. If only some of the ECR needs to be withheld, then the price will match the ECR trigger price.

[^151]: The true floor price is the minimum reserve price, which is lower than the ECR price.

[^152]: Regional Greenhouse Gas Initiative. December 19, 2017. "RGGI 2016 Program Review: Principles to Accompany Model Rule Amendments". _RGGI.org_. Available at [rggi.org/sites/default/files/Uploads/Program-Review/12-19-2017/Principles_Accompanying_Model_Rule.pdf](https://rggi.org/sites/default/files/Uploads/Program-Review/12-19-2017/Principles_Accompanying_Model_Rule.pdf).

[^153]: Regional Greenhouse Gas Initiative. Last accessed August 8, 2023. "Program Review." _RGGI.org_. Available at: [https://www.rggi.org/program-overview-and-design/program-review](https://www.rggi.org/program-overview-and-design/program-review).

[^154]: New Jersey Department of Environmental Protection. Last accessed August 21, 2023. "Regional Greenhouse Gas Initiative." _state.ny.us_. Available at [https://www.state.nj.us/dep/aqes/rggi.html](https://www.state.nj.us/dep/aqes/rggi.html).

[^155]: Virginia Department of Environmental Quality. Last accessed August 21, 2023. "Carbon Trading." _Deq.virginia.gov_. Available at [https://www.deq.virginia.gov/our-programs/air/greenhouse-gases/carbon-trading](https://www.deq.virginia.gov/our-programs/air/greenhouse-gases/carbon-trading).

[^156]: Southern Environmental Law Center. August 21, 2023. "We're suing to hold the line on Virginia's climate progress". Available at: [https://www.southernenvironment.org/news/were-suing-to-hold-the-line-on-virginias-climate-progress/](https://www.southernenvironment.org/news/were-suing-to-hold-the-line-on-virginias-climate-progress/).

[^157]: Pennsylvania Department of Environmental Protection. Last accessed August 21, 2023. "Regional Greenhouse Gas Initiative." _Dep.pa.gov_. Available at [https://www.dep.pa.gov/Citizens/climate/Pages/RGGI.aspx](https://www.dep.pa.gov/Citizens/climate/Pages/RGGI.aspx). See also the recent PA Supreme Court decision, which is under appeal (Huangpu, Kate. "Pa. court strikes down a key climate program, but environmentalists expect an appeal." Spotlight PA. November 1, 2023. Available at [https://www.spotlightpa.org/news/2023/11/regional-greenhouse-gas-rggi-struck-down-pennsylvania-climate-change-fossil-energy/](https://www.spotlightpa.org/news/2023/11/regional-greenhouse-gas-rggi-struck-down-pennsylvania-climate-change-fossil-energy/).

[PDF p. 135 | printed p. 117]

Because the RGGI region includes states not modeled in the AESC 2024 study (New York, Delaware, Maryland, New Jersey, Virginia, and Pennsylvania) and is in fact dominated by emissions outside of New England (see Figure 29)—even in a future where Virigina [sic] and Pennsylvania withdraw from the program—we model the effects of RGGI as an exogenous price rather than a strict cap on emissions. The RGGI price modeled in AESC 2024 is based on historical prices through 2023, an average of historical prices and the ECR trigger price in 2024, and then a trajectory extending the ECR through 2050. This trajectory reflects a future in which reductions in the RGGI cap are continued after the current compliance period ends in 2030. A modeling report from the University of Pennsylvania's Kleinman Center and Resources from the Future also forecasts 2030 RGGI prices at the ECR price (without Pennsylvania).[^158] The report attributes recent high historical RGGI prices to the increase in gas prices, expected to return to previous forecasts by 2025, as well as temporary investor behavior. We observe that prices published as part of RGGI's Third Program Review in September 2023 vary widely according to the scenario being considered.[^159] Although none of the scenarios modeled by RGGI are entirely aligned with the framing used by any of the AESC 2024 counterfactuals and sensitivities, cost projections modeled by RGGI range from (1) being roughly halfway between the RGGI ECR and CCR (as is the case with a flat extension of RGGI's cap, but a regional acceleration to zero-emitting electricity in 2035) to (2) being aligned with the ECR and the AESC 2024 assumption (as is the case with an extension of RGGI's current declining cap, and a regional acceleration to zero-emitting electricity in 2035), to (3) being priced at a near-zero transactional cost, below the ECR (as is the case with a flat extension of RGGI's cap, and a regional acceleration to zero-emitting electricity in 2040).

[^158]: Burtraw, D. et al. "The Prospects for Pennsylvania as a RGGI Member." Resource for the Future and Kleinman Center for Energy Policy at UPenn. May 2023. Available at [https://kleinmanenergy.upenn.edu/wpcontent/uploads/2023/05/Report-23-04.pdf](https://kleinmanenergy.upenn.edu/wpcontent/uploads/2023/05/Report-23-04.pdf).

[^159]: Regional Greenhouse Gas Initiative Program Review: Public Meeting. _RGGI.org_. September 26, 2023. Available at [https://www.rggi.org/sites/default/files/Uploads/Program-Review/2023-09-26/RGGI_26_Sept_2023_Meeting_Presentation.pdf](https://www.rggi.org/sites/default/files/Uploads/Program-Review/2023-09-26/RGGI_26_Sept_2023_Meeting_Presentation.pdf). Slide 28.

[PDF p. 136 | printed p. 118]

**Figure 28. Historical RGGI allowance prices, the prices associated with the cost containment reserve (CCR) and emissions containment reserve (ECR), and RGGI prices used in AESC 2024**

[DIAGRAM DESCRIPTION: Figure 28. Historical RGGI allowance prices, the prices associated with the cost containment reserve (CCR) and emissions containment reserve (ECR), and RGGI prices used in AESC 2024]

A line chart with year on the x-axis (2010 to 2050, ticks every five years) and "Selected RGGI Prices (2024 $/short ton)" on the y-axis (`$0`to` $35`, gridlines every `$5`). Series: (1) a solid black line labeled "Historical" running from 2010 to about 2023; (2) a solid green line with open circular markers labeled "AESC 2024", one marker per year from about 2020 to 2050; (3) a dashed gray line labeled "CCR Price" (the cost containment reserve trigger), from about 2020 to 2030; (4) a dashed gray line labeled "ECR Price" (the emissions containment reserve trigger), from about 2020 to 2030, after which it is not drawn separately because the AESC line follows it. The historical line (values read approximately from the chart, not printed) starts near` $2.80` in 2010, dips to about `$2.50`in 2011-2012, rises to a first peak near` $7` in 2015, falls to about `$4.30`in 2017, climbs to about` $6.50` in 2019, about `$9`in 2021 and peaks at about` $14` in 2022, then falls to about `$13`in 2023. The AESC 2024 line tracks the historical line from 2020 through 2023, then drops to about` $10` in 2024 (the average of historical prices and the ECR trigger price, per the text) and to about `$7.50`in 2025, where it joins the ECR price line; it then rises steadily along the ECR trajectory to about` $24` in 2050. The CCR price line rises from about `$12.50`in 2020 to about` $14.50` in 2021-2022 and about `$21`in 2030; the ECR price line is about` $7` in 2020-2022 and about `$7.50` in 2025. The chart shows that the RGGI price used in AESC 2024 follows recent history, then the ECR trigger price, and stays well below the CCR price throughout.

[→ See original PDF page 136 for visual rendering]

[PDF p. 137 | printed p. 119]

**Figure 29. Electric sector CO₂ emissions in existing and proposed RGGI states, 2022**

[DIAGRAM DESCRIPTION: Figure 29. Electric sector CO₂ emissions in existing and proposed RGGI states, 2022]

A stacked bar chart with four bars on the x-axis ("New England states", "DE, MD, NJ, NY", "VA", "PA") and "2022 electric-sector CO₂ emissions (million short tons)" on the y-axis (0 to 90, gridlines every 10). Each bar is one colour; white horizontal lines divide the New England and "DE, MD, NJ, NY" bars into stacked segments (one per state; segment sizes are not labeled). Bar heights (read approximately from the chart, not printed): New England states about 26 million short tons (dark blue-purple, five or so segments); DE, MD, NJ, NY about 62 (teal, four segments); VA about 27 (green, one segment); PA about 83 (orange, one segment). The chart shows that New England's emissions are small relative to the rest of the actual and proposed RGGI region, with Pennsylvania alone about three times the New England total.

[→ See original PDF page 137 for visual rendering]

_Source: EPA Clean Air Markets Program dataset, available at <https://campd.epa.gov/data/custom-data-download>._

### Massachusetts Global Warming Solutions Act and MassDEP regulations

AESC 2024 models the GHG regulations finalized by the Massachusetts Department of Environmental Protection (MassDEP) in 2017 in accordance with the Massachusetts _Global Warming Solutions Act_ (GWSA). Under this finalized rule, MassDEP established two regulations that impact the electric sector: 310 CMR 7.74, which establishes a state-specific cap on CO₂ emissions from emitting generators in Massachusetts and 310 CMR 7.75, which establishes a Clean Energy Standard for Massachusetts LSEs. Impacts of these policies in $-per-metric-ton terms are available in _Appendix G: Marginal Emission Rates_ .

#### 310 CMR 7.74: Mass-based emissions limit on in-state power plants

310 CMR 7.74 assigns declining limits on total annual GHG emissions from identified emitting power plants within Massachusetts. Table 52 lists the affected power plants under this regulation. In the AESC 2024 study, we modeled this regulation as a state-wide limit through which plants receive CO₂ allowances pursuant to 310 CMR 7.74 at the start of each year.[^160] The emissions limit starts at 9.1

[^160]: We understand that allowances may be distributed through free allocation, through an auction, or through some combination thereof. We do not plan to make a distinction between these approaches in the 2018 AESC study, as the approach is unlikely to substantially impact allowance prices.

[PDF p. 138 | printed p. 120]

million metric tons in 2018, 8.7 million metric tons in 2019 and 8.5 million metric tons in 2020. The limit then declines by about 0.2 million metric tons per year until reaching 1.8 million metric tons in 2050 (see Figure 30).[^161]

In this analysis, we assume that both new and existing units fall under the same aggregate limit. Table 52 lists all the existing units affected by the rule. We assume that both new and existing units are able to fully trade allowances pursuant to 310 CMR 7.74 throughout each compliance year. To simplify computation, we do not model ACPs or banking of CO₂ allowances pursuant to 310 CMR 7.74.

**Figure 30. Analyzed electric sector CO₂ limits under 310 CMR 7.74**

[DIAGRAM DESCRIPTION: Figure 30. Analyzed electric sector CO₂ limits under 310 CMR 7.74]

A line chart with year on the x-axis (2015 to 2050, ticks every five years) and "CO₂ Emissions Limit Under 310 CMR 7.74 (million metric tons CO₂)" on the y-axis (0 to 10, gridlines every 1). A single red line starts at about 9.1 in 2018 and declines almost linearly, to about 8.5 in 2020, about 6.3 in 2030, about 4.0 in 2040 and about 1.8 in 2050 (values read approximately from the chart; the endpoints match the text). The chart shows the steadily declining aggregate cap on Massachusetts power-plant CO₂ emissions.

[→ See original PDF page 138 for visual rendering]

[^161]: For the latest information on limits under 310 CMR 7.74, see Massachusetts Department of Environmental Protection. Proposed Amendments to 310 CMR 7.74. January 4, 2023. Available at [https://www.mass.gov/doc/310-cmr-774-amendments/download](https://www.mass.gov/doc/310-cmr-774-amendments/download), page 3.

[PDF p. 139 | printed p. 121]

**Table 52. List of generating units modeled as subject to 310 CMR 7.74**

| ORSPL | Facility                           | Unit Type | Fuel Type   | EnCompass Unit Name                   |
| ----- | ---------------------------------- | --------- | ----------- | ------------------------------------- |
| 1588  | Mystic                             | ST        | Natural Gas | Mystic Generating Station:7           |
| 1588  | Mystic                             | CC        | Natural Gas | Mystic Generating Station:G941        |
| 1588  | Mystic                             | CC        | Natural Gas | Mystic Generating Station:G942        |
| 1592  | Medway Station                     | GT        | Oil         | Exelon Medway LLC:GT1                 |
| 1592  | Medway Station                     | GT        | Oil         | Exelon Medway LLC:GT2                 |
| 1592  | Medway Station                     | GT        | Oil         | Exelon Medway LLC:GT3                 |
| 59882 | Exelon West Medway II LLC          | GT        | Natural Gas | Exelon West Medway II LLC:GT          |
| 1595  | Kendall Green Energy LLC           | ST        | Natural Gas | Kendall Square Station:JET1           |
| 1595  | Kendall Green Energy LLC           | CC        | Natural Gas | Kendall Square Station:CC1            |
| 1599  | Canal Station                      | ST        | Oil         | Canal:1                               |
| 1599  | Canal Station                      | ST        | Oil         | Canal:2                               |
| 1599  | Canal Station                      | GT        | Oil         | Canal:3                               |
| 1642  | West Springfield                   | ST        | Oil         | Essential Power Massachusetts LLC:3   |
| 1642  | West Springfield                   | GT        | Natural Gas | Essential Power Massachusetts LLC:GT1 |
| 1642  | West Springfield                   | GT        | Natural Gas | Essential Power Massachusetts LLC:GT2 |
| 1660  | Potter                             | CC        | Natural Gas | Potter Station 2:POT2                 |
| 1660  | Potter                             | GT        | Natural Gas | Potter Station 2:GT:52.6MW(2)         |
| 1678  | Waters River                       | GT        | Natural Gas | Waters River:1                        |
| 1678  | Waters River                       | GT        | Natural Gas | Waters River:2                        |
| 1682  | Cleary Flood                       | ST        | Oil         | Cleary Flood:8                        |
| 1682  | Cleary Flood                       | OT        | Natural Gas | Cleary Flood:CC1                      |
| 6081  | Stony Brook                        | CC        | Oil         | Stony Brook:CC1                       |
| 6081  | Stony Brook                        | GT        | Oil         | Stony Brook:1                         |
| 10307 | Bellingham                         | CC        | Natural Gas | Bellingham Cogeneration Facility:CC1  |
| 10726 | MASSPOWER                          | CC        | Natural Gas | Masspower:G321                        |
| 50002 | Pittsfield Generating              | CC        | Natural Gas | Pittsfield Generating LP:CC1          |
| 52026 | Dartmouth Power                    | CC        | Natural Gas | Dartmouth Power Associates LP:CC1     |
| 52026 | Dartmouth Power                    | GT        | Natural Gas | Dartmouth Power Associates LP:GT1     |
| 54586 | Tanner Street Generation, LLC      | CC        | Natural Gas | Tanner Street Generation:CC1          |
| 54805 | Milford Power, LLC                 | CC        | Natural Gas | Milford Power Project:CC1             |
| 55026 | Dighton                            | CC        | Natural Gas | Dighton Power Plant:CC1               |
| 55041 | Berkshire Power                    | CC        | Natural Gas | Berkshire Power:CC1                   |
| 55079 | Millennium Power Partners          | CC        | Natural Gas | Millennium Power:CC01                 |
| 55211 | ANP Bellingham Energy Company, LLC | CC        | Natural Gas | ANP Bellingham Energy Project:CC1     |
| 55212 | ANP Blackstone Energy Company, LLC | CC        | Natural Gas | ANP Blackstone Energy Project:CC1     |
| 55317 | Fore River Energy Center           | CC        | Natural Gas | Fore River Generating Station:G942    |
| 1626  | Salem Harbor                       | CC        | Natural Gas | Salem Harbor Station NGCC:CC1         |
| 1626  | Salem Harbor                       | CC        | Natural Gas | Salem Harbor Station NGCC:CC2         |

_Note: This list includes some units that are modeled as retiring at some point in the study period._

#### 310 CMR 7.75: Clean Energy Standard

This regulation establishes additional tranches of clean energy that are eligible to qualify for Clean Energy Certificates. More information on how we modeled this regulation can be found in Section 4.4: _Renewable energy_ .

[PDF p. 140 | printed p. 122]

### Other environmental regulations and policies

Several other environmental regulations are modeled in EnCompass and are thus embedded in the avoided energy costs. Other environmental regulations not included in the avoided energy costs include the following.

#### Sulfur dioxide, nitrogen oxides, and mercury

Synapse examined allowance prices for annual SO₂ emissions covered under the Cross-State Air Pollution Rule (CSAPR) and the Acid Rain Program (ARP). Actual weighted average allowance prices from the 2022 SO₂ spot auctions are very low, at or around $0.02 per short ton.[^162] Because of this, and because of the relatively small quantity of SO₂ emissions in New England relative to the rest of the country, we do not model any embedded SO₂ prices.

Likewise, we assume no embedded NOₓ prices. This assumption stems from three factors: the New England states being exempt from the CSAPR program; an assumption that currently proposed state-specific regulations in Massachusetts and Connecticut on ozone-season-NOₓ are unlikely to be binding; and NOₓ prices having been excluded from being modeled in previous AESC studies including AESC 2021.

As in past AESC studies, we assumed no trading of mercury and no allowance prices.

#### Other state-specific CO₂ policies

All six New England states have specified a goal or target for reducing CO₂ emissions (see Table 53). Unlike Massachusetts, no other state has currently issued specific electric-sector regulations aimed at requiring that electric-sector emissions remain under a specified cap in some future year. In the AESC 2024 analysis, we do not include any embedded costs of GHG reduction compliance from states other than Massachusetts, and we assume no additional electric-sector regulations to those put forth under 310 CMR 7.74 and 7.75.[^163]

[^162]: U.S. EPA. Last accessed August 10, 2023. "2022 SO₂ Allowance Auction." _EPA.gov_. Available at [https://www.epa.gov/power-sector/2022-so2-allowance-auction#tab-2](https://www.epa.gov/power-sector/2022-so2-allowance-auction#tab-2).

[^163]: Note that AESC 2024 does not assume that the full costs of the Massachusetts GWSA—or any other states' climate goals—are embedded in the energy prices and CES compliance prices. AESC 2021 only models the cost of compliance associated with regulations promulgated by MassDEP, including 310 CMR 7.74 and 310 CMR 7.75. In reality, the full cost of the Massachusetts GWSA and similar goals, targets, and requirements, will also be driven by (a) other, modeled impacts to the electric sector (i.e., new unit retirements, unit additions, natural gas prices, load forecasts) and (b) explicitly non-modeled impacts to the electric sector (i.e., energy efficiency and other DSM programs), (e) [sic] emission-reducing actions that occur outside the electric sector, and will be bounded by (c), the interim targets for specific milestone dates, which are in many cases not yet established.

[PDF p. 141 | printed p. 123]

**Table 53. State-specific GHG emission reduction targets for 2050**

| State | 2050 Target                     | Category         | Sources                                                                                                                                                                                                                                                                                                                     | Interim Targets / Notes                                                                                                                                                                                                                                                                 |
| ----- | ------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CT    | 80% below 2001 levels           | Statutory Target | Substitute House Bill No. 5600 Public Act 08-98: "An Act Concerning Global Warming Solutions" (Global Warming Solutions Act, or GWSA). See <https://www.cga.ct.gov/2008/ACT/PA/2008PA-00098-R00HB-05600-PA.htm>                                                                                                             | Senate Bill No. 7 Public Act No. 18-82: "An Act Concerning Climate Change Planning and Resiliency" established an interim goal of 45% below 2001 levels by 2030. See <https://www.cga.ct.gov/2018/act/pa/pdf/2018PA-00082-R00SB-00007-PA.pdf>                                           |
| ME    | 80% below 1990 levels           | Statutory Target | 38 MRSA §576-A. Greenhouse gas emissions reductions. See <http://www.mainelegislature.org/legis/statutes/38/title38sec576-A.html>                                                                                                                                                                                           | The legislation has the following interim goals: (a) 45% below 1990 levels by 2030; (b) by 2040, the gross annual GHG emissions level must, at a minimum, be on an annual trajectory sufficient to achieve the 2050 annual emissions target; and (c) net zero emissions beginning 2045. |
| MA    | 85% below 1990 levels; Net zero | Statutory Target | Senate Bill No. 9: "An Act Creating A Next-Generation Roadmap for Massachusetts Climate Policy" (2021 Climate Law). See <https://www.mass.gov/doc/final-signed-letter-of-determination-for-2050-emissions-limit/download> and <https://www.mass.gov/doc/2025-and-2030-ghg-emissions-limit-letter-of-determination/download> | The Executive Office of Energy and Environmental Affairs (EEA) has set the following interim goals: (a) 33% below 1990 levels by 2025 and (b) 50% below 1990 levels by 2030. The EEA is also required to set a 2040 reduction goal of at least 75% below 1990 levels.                   |
| NH    | 80% below 1990 levels           | Executive Target | 2009 New Hampshire Climate Action Plan. See <https://www.des.nh.gov/organization/divisions/air/tsb/tps/climate/action_plan/documents/nhcap_final.pdf>                                                                                                                                                                       | n/a                                                                                                                                                                                                                                                                                     |
| RI    | Net zero                        | Statutory Target | Title 42, State Affairs and Government, Chapter 42-6.2 Resilient Rhode Island Act of 2014 – Climate Change Coordinating Council, Section 42-6.2-2. See <http://webserver.rilin.state.ri.us/Statutes/TITLE42/42-6.2/42-6.2-2.HTM>                                                                                            | The legislation has the following interim goals: (a) 45% below 1990 levels by 2030 and (b) 80% below 1990 levels by 2040.                                                                                                                                                               |
| VT    | 80% below 1990 levels           | Statutory Target | Title 10 V.S.A. § 578 Conservation And Development Chapter 023: Air Pollution Control. See <https://legislature.vermont.gov/statutes/section/10/023/00578>                                                                                                                                                                  | The legislation has the following interim goals: (a) 26% below 2005 levels by 2025 and (b) 40% below 1990 levels by 2030.                                                                                                                                                               |

_Note: "Category" uses definitions from <https://www.c2es.org/document/greenhouse-gas-emissions-targets/>._

[PDF p. 142 | printed p. 124]

#### Massachusetts sector-based sublimits

The 2021 Climate Law in Massachusetts directed the Executive Office of Energy and Environmental Affairs (EEA) to adopt sector-specific emissions sublimits for every five years between 2020 and 2050.[^164] These sublimits are intended to complement the state's economy-wide emissions limits, targeting the following sectors: electric power, transportation, C&I heating and cooling, residential heating and cooling, industrial processes, and natural gas.

The electric power sector emissions category includes the combustion of fuels in power plants located in Massachusetts as well as emissions from electricity generated in or imported into ISO New England to meet Massachusetts' electricity demand. These totals also take into account renewable and clean energy credits from the state's Renewable Portfolio Standard and Clean Energy Standards. The heating and cooling sectors include all onsite combustion of fuels. The natural gas emissions sector represents fugitive emissions from natural gas distribution and service. The Massachusetts _Clean Energy and Climate Plan for 2025 and 2030_ provides details on the sector-based sublimits for 2025 and 2030, and the _Clean Energy and Climate Plan for 2050_ provides these details for 2050.[^165][^166] The emission sublimits relevant to the sectors addressable by programmatic DERs are shown in Table 54.[^167]

**Table 54. Sector-based sublimits describing required emission reductions relative to 1990 levels**

|      | Residential heating and cooling | Commercial and industrial heating and cooling | Electric Power |
| ---- | ------------------------------: | --------------------------------------------: | -------------: |
| 2025 |                             29% |                                           35% |            53% |
| 2030 |                             49% |                                           49% |            70% |
| 2050 |                             95% |                                           92% |            93% |

_Sources: <https://www.mass.gov/doc/2025-and-2030-ghg-emissions-limit-letter-of-determination/download> and <https://www.mass.gov/doc/determination-letter-for-the-2050-cecp/download>._

The following sections describe how we modeled these sublimits for AESC 2024. We note that, although these calculations have been performed for Massachusetts, we believe that an analogous methodology is appropriate to be applied to any other states with emissions limits or sublimits, or any other states with Clean Heat Standards similar to the one proposed in Massachusetts.

[^164]: Senate Bill No. 9, 2021: "An Act Creating A Next-Generation Roadmap for Massachusetts Climate Policy", available at [https://malegislature.gov/Bills/192/S9/BillHistory](https://malegislature.gov/Bills/192/S9/BillHistory).

[^165]: Massachusetts _Clean Energy and Climate Plan for 2025 and 2030_, available at [https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-plan-for-2025-and-2030](https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-plan-for-2025-and-2030).

[^166]: Massachusetts _Clean Energy and Climate Plan for 2050_, available at [https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-plan-for-2050](https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-plan-for-2050).

[^167]: We note that there are other sectors with sublimits (e.g., transportation, natural gas distribution & service, and industrial processes). However, these are not considered in AESC 2024 because the Massachusetts program administrators do not currently offer measures or programs that address emissions in these sectors.

[PDF p. 143 | printed p. 125]

##### Electric sector

AESC 2024 does not explicitly model compliance with the electric sector sublimit. Instead, we observe the emission reductions modeled in the EnCompass model for Massachusetts and compare these with the emission levels required by the sublimits. This is done due to the number of policies that are already deployed in Massachusetts that either purposefully or indirectly achieve emission reductions over time, even without electric energy efficiency (including 111, RGGI, 310 CMR 7.74 and 310 CMR 7.75, and various other renewable policies). Figure 31 shows the emissions modeled in Counterfactual #1. The components of this figure are estimated as follows:

- The red "electric sector GHG sublimits" represent the quantity of allowable GHG emissions in the electric sector, for Massachusetts. These values are defined for 2025, 2030, and 2050 in terms relative to the 1990 level of emissions (see Table 54). All other values are interpolated (except 2024, which re-uses the 2025 level of emissions).
- The yellow "310 CMR 7.74" series describes the cap on in-state emissions from most of the large electric sector power plants in Massachusetts.
- The dark blue "in-state emissions" series is calculated by summing the total emissions from the power plants located in Massachusetts' borders. The emissions in this category are primarily made of up [sic] those generated by power plants affected by 310 CMR 7.74, but includes emissions from other unaffected plants as well.
- The light blue "imported emissions" series is calculated via an algorithm which seeks to approximate the one used by Massachusetts DEP in its GHG emissions inventory.[^168] Briefly, imported emissions are equal to total imported load multiplied by a marginal emissions rate, where the marginal emissions rate is the rate defined in Section 8.2: _Applying non-embedded costs_, and total imported load is estimated by subtracting the sum of the generation from in-state emitters and purchased RECs (and REC-like instruments) from the projected Massachusetts load.

Table 55 summarizes the degree to which the electric sector complies with the electric sector sublimit (overcompliance is shown with positive numbers and non-compliance is shown with negative numbers).

[^168]: See [https://www.mass.gov/lists/massdep-emissions-inventories](https://www.mass.gov/lists/massdep-emissions-inventories) for more information.

[PDF p. 144 | printed p. 126]

**Figure 31. Modeled Massachusetts emissions in Counterfactual #1, compared to electric sector sublimits**

[DIAGRAM DESCRIPTION: Figure 31. Modeled Massachusetts emissions in Counterfactual #1, compared to electric sector sublimits]

A combined area-and-line chart with year on the x-axis (labeled ticks 2024, 2029, 2034, 2039, 2044, 2049) and "Total MA GHG Emissions (short tons CO2e)" on the y-axis (0 to 16, ticks every 2; the unit is printed without a "million" prefix). Series and labels as printed on the chart: a red dashed line with large red dots, labeled "Electric sector GHG sublimits" (dots at 2024 at about 14.5, about 2030 at about 9, and about 2050 at about 2.2, with a dashed straight-line interpolation between them); a solid yellow/orange line labeled "310 CMR 7.74", declining from about 8.4 in 2024 to about 2 in 2050; stacked areas below the yellow line in teal shades: a light blue band labeled "Imported emissions" (on top) and a dark teal area labeled "In-state emissions". A further label printed inside the chart, "Exported emissions", has an arrow pointing to the teal areas around 2030 [source discrepancy: the text describes only "in-state emissions" and "imported emissions" series; no "exported emissions" series is described]. Total modeled emissions fall from about 8 in 2024 to well under 2 by 2050, staying below the electric sector sublimit line in every year, consistent with the positive "overcompliance" values in Table 55 (values read approximately from the chart, not printed).

[→ See original PDF page 144 for visual rendering]

**Table 55. Difference in electric sector GHG emissions, compared to electric sector sublimits (million short tons CO₂e)**

|      | CF #1 | CF #2 | CF #3 | CF #4 | CF #5 | CF #6 |
| ---- | ----: | ----: | ----: | ----: | ----: | ----: |
| 2024 |   6.0 |   5.5 |   6.0 |   6.1 |   6.1 |   6.1 |
| 2025 |   6.4 |   7.3 |   6.3 |   6.5 |   6.5 |   6.5 |
| 2026 |   6.2 |   6.9 |   6.0 |   6.3 |   6.3 |   6.3 |
| 2027 |   6.2 |   6.7 |   6.0 |   6.3 |   6.3 |   6.3 |
| 2028 |   6.2 |   5.2 |   5.9 |   6.2 |   6.2 |   6.2 |
| 2029 |   6.5 |   6.3 |   6.5 |   6.6 |   6.6 |   6.6 |
| 2030 |   6.8 |   6.6 |   6.7 |   6.8 |   6.8 |   6.8 |
| 2031 |   6.3 |   6.1 |   6.2 |   6.4 |   6.4 |   6.4 |
| 2032 |   6.1 |   6.1 |   6.0 |   6.1 |   6.1 |   6.1 |
| 2033 |   5.6 |   5.7 |   5.4 |   5.6 |   5.6 |   5.7 |
| 2034 |   5.2 |   5.4 |   5.0 |   5.1 |   5.1 |   5.3 |
| 2035 |   4.8 |   4.9 |   4.6 |   4.9 |   4.8 |   4.8 |
| 2036 |   4.6 |   4.9 |   4.4 |   4.7 |   4.6 |   4.7 |
| 2037 |   4.1 |   4.7 |   4.0 |   4.4 |   4.3 |   4.3 |
| 2038 |   4.1 |   4.3 |   3.7 |   4.0 |   4.1 |   3.9 |
| 2039 |   4.0 |   4.2 |   3.9 |   4.1 |   4.1 |   4.0 |
| 2040 |   3.6 |   3.8 |   3.5 |   3.7 |   3.7 |   3.5 |
| 2041 |   3.6 |   3.7 |   3.4 |   3.5 |   3.7 |   3.4 |
| 2042 |   3.1 |   3.3 |   3.1 |   3.1 |   3.3 |   3.0 |
| 2043 |   3.1 |   3.3 |   3.1 |   3.2 |   3.3 |   3.0 |
| 2044 |   2.8 |   2.9 |   2.7 |   2.8 |   2.9 |   2.7 |
| 2045 |   2.8 |   3.0 |   2.8 |   2.8 |   2.9 |   2.6 |
| 2046 |   2.7 |   2.9 |   2.7 |   2.8 |   2.8 |   2.7 |
| 2047 |   2.6 |   2.7 |   2.6 |   2.7 |   2.7 |   2.6 |
| 2048 |   2.2 |   2.4 |   2.3 |   2.3 |   2.4 |   2.2 |
| 2049 |   2.2 |   2.3 |   2.2 |   2.2 |   2.3 |   2.2 |
| 2050 |   2.0 |   2.2 |   2.1 |   2.1 |   2.2 |   2.1 |

_Note: Overcompliance with sublimits is shown with positive numbers; undercompliance is shown with negative numbers._

##### Building sectors

AESC 2024 posits that the mechanisms most likely to achieve compliance with emission reductions required in the residential, commercial, and industrial heating sectors are (a) energy efficiency, (b)

[PDF p. 145 | printed p. 127]

building electrification, and (c) renewable fuels. We assume that counterfactuals that do not achieve the emission sublimits for these sectors via the first two mechanisms must implement a sufficient quantity of renewable fuels in order to reduce emissions in each year and achieve compliance.[^169] Because most modeled counterfactuals do not include quantities of either energy efficiency or building electrification sufficient to meet the sublimit requirements, each counterfactual therefore requires some level of blending of renewable fuels alongside direct fuels (namely natural gas, home heating oil, and propane).

The Synapse Team developed a projection of business-as-usual (BAU) fuel use and emissions in Massachusetts for each fuel type and sector, based on applying growth rates from AEO 2023 to recent historical fuel use data reported by EIA in the SEDS database. For each counterfactual, we then adjust this BAU projection to account for the reduced fuel use (and emissions) achieved via the energy efficiency and building electrification measures that are included. Next, we calculate the amount of renewable fuel blending needed in each year that would achieve emission reductions equal to the remaining gap.[^170] Finally, we adjust this blending requirement to reflect any over-compliance or under-compliance in the electric sector.

For example, Counterfactual #1 does not assume any future energy efficiency or building electrification measures beyond that which is installed in 2023; this scenario therefore requires relatively high levels of renewable fuel blending. This level of renewable fuel blending is decreased by the quantity of over-compliance in the electric sector.

Meanwhile, Counterfactual #3 includes large amounts of building electrification. These building electrification measures achieve a large quantity of emission reductions on their own, necessitating a comparatively lower level of fuel blending in order to achieve compliance with the emission sublimits. As with Counterfactual #1, we observe overcompliance with the electric sector sublimits in all years, which helps to reduce the quantity of renewable fuel blending required. This level of renewable fuel blending is decreased by the quantity of over-compliance in the electric sector. Figure 32 illustrates the estimated fuel blending requirements for each counterfactual.

[^169]: We note that this is the principle underlying the proposed Clean Heat Standard, a policy that is currently under development by Massachusetts Department of Environmental Protection (for more on this topic, see [https://www.mass.gov/info-details/massachusetts-clean-heat-standard](https://www.mass.gov/info-details/massachusetts-clean-heat-standard)). As of October 2023, details of a proposed Clean Heat Standard have not yet been made public, although we understand such detail is likely to be issued in 2024. Therefore, the analysis described in this section should be considered an estimation of the likely cost impacts of the coming Clean Heat Standard, without a focus on the specific details of how the policy is likely to be implemented.

[^170]: As with electric sector emissions, sublimits for the residential heating and C&I heating sectors are only available for 2025, 2030, and 2050. Sublimits for all other years have been linearly interpolated.

[PDF p. 146 | printed p. 128]

**Figure 32. Renewable fuel blending requirements for Counterfactual #1 and Counterfactual #5**

[DIAGRAM DESCRIPTION: Figure 32. Renewable fuel blending requirements for Counterfactual #1 and Counterfactual #5]

A line chart with year on the x-axis (2024 to 2050, labeled every two years) and "Biofuel blending required (%)" on the y-axis (0% to 100%, gridlines every 20%). Two lines: a teal line labeled "CF #1" and an orange line labeled "CF #5". Both are at 0% from 2024 until about 2028-2029. CF #1 then rises steadily, to roughly 20% around 2034, about 40% around 2038, about 60% around 2043 and about 85% in 2050. CF #5 stays at 0% until about 2031, then rises more slowly, to roughly 20% around 2038, about 40% around 2043 and about 70% in 2050 (values read approximately from the chart, not printed). The chart shows that renewable-fuel blending required for compliance with the building-sector sublimits is much higher without building electrification (CF #1) than with it (CF #5).

[→ See original PDF page 146 for visual rendering]

_Note: In general, counterfactuals that feature building electrification (Counterfactual #3, Counterfactual #4, Counterfactual #6) have projections that closely resemble the projection for Counterfactual #5, will those that do not (Counterfactual #2) resemble Counterfactual #1._ [sic: "will" for "while"]

Using the Excel-based versions of AESC 2024's Appendix C and Appendix D, users can calculate the avoided costs for natural gas and fuel oils in Massachusetts both with and without the renewable fuel blending requirements. Generally speaking, these fuel blending requirements increase avoided costs for natural gas and fuel oils (thereby highlighting the relative cost-effectiveness of energy efficiency and building electrification measures, relative to renewable fuels). Using the Excel-based AESC 2024 User Interface, users can also calculate how these blending requirements impact avoided costs associated with non-embedded GHG costs and DRIPE. Generally speaking, including these blending requirements reduces the avoided costs for these categories, as renewable fuels are assumed to have zero (or near-zero) emissions, and are not calculated as having DRIPE benefits.[^171] More information on the assumptions related to renewable fuel costs, potentials, and emission rates can be found in Section 2.3: _New England natural gas market_ and Section 3.4: _Avoided costs_. More information on the results associated with blending renewable fuels into avoided costs of natural gas and fuel oils can be found in Section 2.5: _Avoided natural gas costs by end_ use and Section 3.4: _Avoided costs_.

#### U.S. EPA's proposed carbon emission rule for fossil-fuel-fired power plants

In May 2023, U.S. EPA released its proposed _Greenhouse Gas Standards and Guidelines for Fossil Fuel-Fired Power Plants_ under section 111 of the _Clean Air Act_. Under the proposed rule, different carbon emission abatement pathways are available depending on an affected power plant's retirement date, size, and capacity factor. Table 56 summarizes compliance pathways under 111(d), which regulates existing fossil plants, and Table 57 summarizes compliance pathways under 111(b), which regulates new gas plants (there are currently no planned new coal plants in New England or the United States).

[^171]: It is likely that eventual large-scale markets for renewable fuels do have DRIPE benefits, but due to the nascent nature of these markets, and the uncertainty in estimating a DRIPE value, we have assumed DRIPE benefits to be zero.

[PDF p. 147 | printed p. 129]

**Table 56. Compliance options for existing power plants under EPA's proposed 111(d) rule**

| Unit Type                                                               | Retirement Date                            | Compliance Pathway                                                                                |
| ----------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Coal and Oil/Gas Steam                                                  | Before 2032                                | Plants must not exceed current emissions rate                                                     |
|                                                                         | After 2032 but before 2035                 | Capacity factor must be less than or equal to 20% in 2030; must not exceed current emissions rate |
|                                                                         | After 2035 but before 2040                 | Units must co-fire natural gas at 40% of heat input in 2030                                       |
|                                                                         | After 2040 or no announced retirement date | Units must have 90% CCS in 2030; wet FGD and ELG also required                                    |
| Gas GTs and CCs with capacity > 300 MW and future capacity factor > 50% | -                                          | Path A: 90% CCS by 2035; Path B: Combust 30% H₂ by volume by 2032, 96% H₂ by 2038                 |
| All other gas-fired GTs and CCs                                         | -                                          | No controls needed                                                                                |

_Extractor note (not source text): in the PDF the "Unit Type" cell "Coal and Oil/Gas Steam" spans its four retirement-date rows; it is printed once here, with the continuation rows' cells left blank. In the "Gas GTs and CCs" row, "Path A" and "Path B" are on separate lines in the PDF cell._

**Table 57. Compliance options for new gas plants under EPA's Proposed 111(b) rule**

| Unit Type                  | Capacity Factor Cap | Compliance Pathway                                                   |
| -------------------------- | ------------------- | -------------------------------------------------------------------- |
| Peaking (likely GTs)       | 20%                 | No controls needed (emissions rate equal to efficient plant in 2023) |
| Intermediate (CCs and GTs) | 50%                 | Combust 30% H₂ by volume by 2032                                     |
| Baseload (likely CCs only) | -                   | Combust 30% H₂ by volume by 2032, 96% H₂ by 2038                     |

In New England's existing fleet of fossil plants, there are 13 gas-fired combined combined-cycle [sic] units that may be affected by the proposed 111(b).[^172] For each of these units, we allow the model to optimize between Path A (CCS) and Path B (hydrogen blending) outlined in Table 56. There are no coal plants expected to be impacted by 111(b), and there are unlikely to be any simple-cycle combustion turbines that would be affected by 111(b).[^173]

[^172]: Each of these units has a capacity equal to or greater than the 300-MW threshold stated in EPA's proposed rule. Many, but not all of the units, have a historical capacity factor greater than the 50 percent capacity threshold. If these plants exceed a capacity factor of 50 percent in the relevant years, they will incur compliance requirements.

[^173]: We note that Canal 3 is likely the only simple-cycle combustion turbine that exceeds EPA's size threshold; but given its relatively low historical capacity factor (about 5 percent), it is unlikely to incur any compliance requirements.

[PDF p. 148 | printed p. 130]

**Table 58. List of existing gas plants subject to proposed 111 rules**

| Plant Type         | Plant Name                    | ORSPL | Unit ID | Plant State | 2021 Capacity (MW) | 2021 Capacity Factor (%) | Likely to trigger 111 compliance based on 2021 operation? |
| ------------------ | ----------------------------- | ----- | ------- | ----------- | -----------------: | -----------------------: | --------------------------------------------------------- |
| Combustion Turbine | Canal                         | 1599  | 3       | MA          |                330 |                       5% | No                                                        |
| Combined Cycle     | Millennium Power              | 55079 | CT01    | MA          |                335 |                      24% | No                                                        |
| Combined Cycle     | Granite Ridge                 | 55170 | CT11    | NH          |                339 |                      53% | Yes                                                       |
| Combined Cycle     | Granite Ridge                 | 55170 | CT12    | NH          |                339 |                      55% | Yes                                                       |
| Combined Cycle     | Fore River Generating Station | 55317 | GT11    | MA          |                364 |                      52% | Yes                                                       |
| Combined Cycle     | Fore River Generating Station | 55317 | GT12    | MA          |                362 |                      58% | Yes                                                       |
| Combined Cycle     | CPV Towantic Energy Center    | 56047 | CTG1    | CT          |                389 |                      81% | Yes                                                       |
| Combined Cycle     | CPV Towantic Energy Center    | 56047 | CTG2    | CT          |                390 |                      82% | Yes                                                       |
| Combined Cycle     | Kleen Energy Systems Project  | 56798 | U1      | CT          |                311 |                      43% | No                                                        |
| Combined Cycle     | Kleen Energy Systems Project  | 56798 | U2      | CT          |                311 |                      46% | No                                                        |
| Combined Cycle     | Bridgeport Station            | 568   | 501     | CT          |                576 |                      73% | Yes                                                       |
| Combined Cycle     | Salem Harbor Station NGCC     | 60903 | 3       | MA          |                339 |                      11% | No                                                        |
| Combined Cycle     | Salem Harbor Station NGCC     | 60903 | 4       | MA          |                338 |                      14% | No                                                        |

_Notes: This table shows only the combustion turbine components of any combined cycle plants. Each of these rows has been allocated a share of the capacity and generation at the local steam recovery units, based on 2021 data from EPA's NEEDS database and EIA 923. Units at Merrimack and Mystic Generation are not shown, as these units are assumed to retire in May 2026 and June 2024, respectively (see Table 45 and Table 47). All plant attributes used in identifying which plants are likely to be subject to 111 is based on EPA's April 2023 edition of the NEEDS database, available at <https://www.epa.gov/system/files/documents/2023-04/NEEDS%20for%20EPA%20Post-IRA%202022%20Reference%20Case.xlsx>. Plants are flagged as "likely to trigger 111 compliance based on 2021 operation" if they have a capacity factor higher than 50 percent._

New gas plants that operate with a capacity factor greater than 20 percent will eventually require either some amount of hydrogen blending or CCS equipment. Both of these technologies have significant cost uncertainties.

For the hydrogen-enabled plants, we use an exogenous hydrogen price trajectory and do not model hydrogen production explicitly (see projection developed in Section 2.3: _New England natural gas market_). Our modeling does not dynamically model electrolyzers and the incremental renewable energy required to produce the hydrogen, but rather integrates all costs into the hydrogen fuel price trajectory. If we were to dynamically model hydrogen, we would need to calculate a shadow price of hydrogen which would vary by scenario (depending on electricity prices and electrolyzer utilization). Using a set

[PDF p. 149 | printed p. 131]

price trajectory allows us to be consistent across scenarios, and with other avoided fuel cost calculations.

For new and existing baseload gas plants that install CCS, we model all relevant retrofit costs, CO₂ transportation and storage costs, and parasitic load effects associated with operating CCS equipment, as well as the IRA section 45Q tax credits available to powerplants that capture CCS.

For both hydrogen blending and CCS, we use the same retrofit cost assumptions used by the EPA to analyze the impact of its proposed rule through its Regulatory Impact Analysis.[^174]

EPA is currently accepting comments on the proposed rule and expects to publish a final rule by summer 2024. The rule may be challenged on the grounds that the proposed systems of emission reduction have not been "adequately demonstrated" as required under Section 111 of the _Clean Air Act_. However, the current policy environment, including the IRA 45Q tax credit for capturing CO₂ and the IRA 45V tax credit for producing hydrogen, will likely lend support to arguments in favor of the economic feasibility of these measures. Generator owners and operators will face decisions now regarding whether to retire fossil units and how to plan for future generation. If the judicial review ends up taking a few years, the regulatory uncertainty may be great enough to cause operators to retire sources early and begin planning their systems assuming the rule will go through regardless of the final outcome.[^175]

### Inflation Reduction Act and Bipartisan Infrastructure Law

The IRA and Bipartisan Infrastructure Law (BIL) were passed in August 2022 and November 2021 respectively. Both laws allocate substantial federal funding to accelerate the energy transition over the next decade. The tax credits in the IRA begin to phase out after 2032, if and only if the U.S. electric sector emissions reach 25 percent of 2022 levels. We assume that the tax credits remain in effect throughout the study period. The most relevant elements of these laws for the AESC modeling will be:

1. Tax credits for renewable energy resources: Applicable IRA tax credits are included in the methodology for projecting renewable energy builds (see Chapter 7. _Avoided Cost of Compliance with Renewable Portfolio Standards and Related Clean Energy Policies_ for more information).
2. Tax credits for hydrogen production and CCS: We assume IRA hydrogen production tax credits are represented in the projected hydrogen fuel price trajectory. Power plants that capture CO₂ receive commensurate IRA tax credit amounts.
3. Tax credits for nuclear power production: We assume the IRA 45U zero-emission production tax credit for existing nuclear powerplants prevents the two nuclear

[^174]: EPA. _Regulatory Impact Analysis_. Docket EPA-HQ-OAR-2023-0072. Available at: [https://www.regulations.gov/document/EPA-HQ-OAR-2023-0072-0007](https://www.regulations.gov/document/EPA-HQ-OAR-2023-0072-0007).

[^175]: Clements, Carter. 2023 "Expect Legal Challenges to New EPA Rules on Emissions". _Power Magazine_. Available at: [https://www.powermag.com/expect-legal-challenges-to-new-epa-rules-on-emissions/](https://www.powermag.com/expect-legal-challenges-to-new-epa-rules-on-emissions/)

[PDF p. 150 | printed p. 132]

powerplants in New England (Seabrook and Millstone) from retiring during our study period.

4. Funding for energy efficiency and electrification measures: This funding has the potential to impact future load. All of our assumptions are based on the most recent data from ISO New England, which to our best understanding does not currently include impacts any impacts [sic] from IRA or BIL.[^176] Because most states in New England already have ambitious energy efficiency and electrification plans, it is unclear whether the IRA funding would lead to different amounts of energy efficiency and electrification, or whether this funding would instead decrease realized costs for consumers. Meanwhile, for electric vehicles, we observe that recent studies analyzing the impact of the IRA suggest that, with IRA funding, electric vehicle sales shares might reach levels of about 50–60 percent in the early 2030s.[^177] Using a standard adoption S-Curve and typical rates of vehicle turnover, that implies electric vehicles make up about 20–30 percent of vehicle stock by the early 2030s and reach close to 100 percent stock by 2050. This resembles the forecasts that ISO New England have assembled for the six states in its CELT 2023 forecast, which are used in this AESC analysis.[^178]

[^176]: Because of limitations in this study's scope and budget, we do not include further impacts on load related to IRA or BIL.

[^177]: _Analyzing the Impact of the Inflation Reduction Act on Electric Vehicle Uptake in the United States_. Slowik et. al. ICCT and Energy Innovation. January 2023. Available at [https://theicct.org/wp-content/uploads/2023/01/ira-impact-evs-us-jan23.pdf](https://theicct.org/wp-content/uploads/2023/01/ira-impact-evs-us-jan23.pdf).

[^178]: See Section 4.3: _New England system demand and energy components_ for more information on these forecasts.

[PDF pp. 151-436 not transcribed: Chapter 5 (Avoided Capacity Costs) onward, i.e. Chapters 5-12 and Appendices A-K, in the other files of this folder (see README.md)]
