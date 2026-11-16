# Plan: when the distribution system becomes winter peaking

Implemented in `distribution_system_winter_peak.qmd`. This file is the spec the notebook follows.

The question stays the same. How many residential heat-pump retrofits does it take before the Company's distribution system, taken as a whole, is winter peaking? Winter peaking means the winter peak is higher than the summer peak. The system is the hourly sum of load across the Company's distribution substations in OCC-733 Attachment 1. This is not a substation or feeder result.

## What the notebook will report

For each heating group that can be retrofitted, one count: the number of homes of that group, added one at a time to today's system, at which the winter peak rises above the summer peak. The groups are natural gas, propane, oil, wood, and electrical resistance. Each group is its own experiment. Homes already on a heat pump are not added.

Alongside the count, the notebook will show the summer peak and the winter peak at that count, both in megawatts on the 2025 average-load scale from step 1. If a group runs out of homes before the winter peak passes the summer peak, the result is that the group does not flip the system.

## Step 1. Scale each earlier year to the 2025 average load

This step is already in the notebook and stays.

OCC-733 Attachment 1 is one row per hour from January 1, 2022 through December 31, 2025. The series is `total_mw`, the metered sum across distribution substations. `net_load_mw` stays unused.

For each of 2022, 2023, and 2024, multiply every hour by one factor:

```text
factor(year) = (mean of total_mw in 2025) / (mean of total_mw in that year)
```

2025 is multiplied by 1. After this, the average hour of each year equals the average hour of 2025. February 29, 2024 is kept, so 2024 still has 8,784 hours and the other years have 8,760. The scaled values stay in megawatts. Call this series `load_mw_2025`.

## Step 2. Fit a system KDE in each of the 576 cells

This step is already in the notebook and stays, with one change of kernel stated below.

Label every scaled hour by month (1–12), hour beginning (0–23), and day type. A day is `weekend_holiday` when it is a Saturday, a Sunday, or one of the eleven federal holidays, with a Saturday holiday observed on the Friday before and a Sunday holiday observed on the Monday after. That is the calendar in `probability_of_peak.py` (`label_hour_types`, `DAY_TYPES`). The other day type is `weekday`. These labels are the 576 cells: 12 × 24 × 2.

In each cell, the sample is `load_mw_2025` for every hour that falls in that cell, across 2022–2025. The unscaled `total_mw` is not the sample. Nothing is averaged across years or across hours before the fit. A cell has from 35 to 89 hours.

Fit one Gaussian kernel density to that sample:

- Kernel: `scipy.stats.gaussian_kde`, the density `kde_sum.py` knows how to add.
- Bandwidth: Scott's rule, the `gaussian_kde` default. The same rule as `scott_bandwidth` in `probability_of_peak.py`.
- The kernel is not truncated. The probability-of-peak routine cuts each kernel at three bandwidths and renormalizes. That truncated density is a different object, and `SumKDE` does not add truncated kernels. Both densities in the sum use the untruncated Scott kernel so the sum is the one `SumKDE` defines.

The fitted object for a cell is the sample and the bandwidth. No draws are stored. Call this density `X(cell)`. It is in megawatts.

## Step 3. Fit a change KDE for each heating group, in each of the 576 cells

The homes are the Eversource buildings in ResStock 2024.2, the same sample the notebook already loads (`STATE = "CT"`, `BATCH = "ct_20261015_a"`, `UTILITY = "ct_eversource"`).

The heating group comes from upgrade 00, the baseline, and it stays on the building after the retrofit. Upgrade 00 grid consumption is the precalc segment `default_ry1_r1_uncalibrated`. Upgrade 02 grid consumption is the calibrated segment of that same run, which is the heat-pump retrofit the notebook already uses. Both files are on the same clock and the same building ids. The consumption is `grid_cons_kwh`: kilowatt-hours taken from the grid in that hour, after rooftop solar, floored at zero.

Group assignment, in this order, so each building is in one group:

| Group | Rule on the upgrade-00 metadata |
| --- | --- |
| Heat pump | `postprocess_group.heating_type_v2 == "heat_pump"` |
| Electrical resistance | `heating_type_v2 == "electrical_resistance"` |
| Natural gas | `heating_type_v2 == "natgas"` |
| Oil | `heats_with_oil` |
| Propane | `heats_with_propane` |
| Wood | everything else (`heating_type_v2 == "other"`, fuel Other Fuel or None) |

ResStock has no wood flag. Wood means that remainder, which is how the notebook treats wood today.

The clock. ResStock simulated these homes on 2018 weather. The CAIRO file stamps those hours as 2025 in UTC, five hours ahead of Eastern Standard Time. Shift them back onto the 2018 local calendar, as the notebook already does, and label month, hour, and day type with the same weekend-and-holiday rule as the system load. A January weekday hour 18 in the home sample is the same cell as a January weekday hour 18 in the OCC-733 sample.

For each building and each of the 8,760 hours:

```text
change_kwh = grid_cons_kwh(upgrade 02) − grid_cons_kwh(upgrade 00)
```

That difference is the paired change for that building in that hour. It is already in kilowatts for a one-hour period.

For each heating group and each of the 576 cells, the KDE sample is every one of those paired differences whose hour falls in the cell, from every building in the group. A building is not collapsed to its average in the cell first. If a cell contains H hours of the year and the group has N buildings, the sample has N × H points. Every building contributes the same H, because the sample is one weather year and the cell is a clock type.

Fit the same untruncated Scott Gaussian KDE as in step 2. One density per group per cell. Call it `Y(group, cell)`. Divide by 1,000 so it is in megawatts before it is added to `X`. Buildings are equally weighted. ResStock sample weights are not used.

The heat-pump group's change density is fit and kept for inspection. Those homes are already on a heat pump, so step 6 does not add them.

This is the part of step 3 that is new. The notebook today reduces each building to one number per cell, the average of its hours in the cell, and fits the density across buildings. The sample here is the hourly differences themselves.

## Step 4. Add the house density to the system density, cell by cell

Adding one home of a given group replaces the load density in each cell with the sum of the two densities in that same cell:

```text
Z_1(cell) = X(cell) + Y(group, cell)
```

`X` and `Y` are independent. The density of the sum is the convolution in `kde_sum.SumKDE`: a Gaussian mixture with one equally weighted component at every pairwise sum of a system sample point and a change sample point, and with variance equal to the sum of the two bandwidths squared. The mean of the sum is the sum of the means.

The cells are aligned. The January weekday hour-18 system density is added only to the January weekday hour-18 change density. A home added to one cell is the same count of homes in every cell: one retrofit changes all 576 cells together.

A second home of the same group is another independent copy of `Y`:

```text
Z_k(cell) = X(cell) + Y_1(group, cell) + … + Y_k(group, cell)
```

Homes from other groups are not in this sum. Each group is a separate experiment, starting again from `X`.

## Step 5. One percentile of each cell is the peak input

One variable, `peak_quantile`, sets the percentile. It is a probability between 0 and 1. The default is `0.90`. Changing it is the only edit required to use the 95th percentile, or any other percentile, everywhere below: every cell, both seasons, and the crossing count.

For a given group and a given count of homes k, take that percentile of `Z_k(cell)` in every cell. That is the load, in megawatts, assigned to that cell. Call it `q(cell, k)`.

The summer peak at that count is the largest `q` among cells whose month is June, July, August, or September. The winter peak is the largest `q` among cells whose month is December, January, or February. Day type and hour are both free inside the season, so the cell that sets the peak can change as homes are added.

At k = 0, `Z_0` is the system density `X` alone, and the same rule gives today's summer and winter peaks on this definition. Today's peaks are these percentiles of `load_mw_2025`, on the scaled series. They are a different number from the highest metered hour in each season, which is what the notebook reports now.

Winter peaking at count k means:

```text
winter peak(k) > summer peak(k)
```

## Step 6. Add homes one at a time until the peak flips

For each of natural gas, propane, oil, wood, and electrical resistance:

1. Start at k = 0, with the system densities only.
2. Add one home: replace `Z` with `Z` convolved with that group's `Y`, in all 576 cells.
3. Recompute the 576 percentiles at `peak_quantile`, then the summer peak and the winter peak.
4. The result is the smallest whole number k at which the winter peak is above the summer peak.

Every home in a group has the same change density, so the order of homes inside the group does not matter. The count is a count of homes, and each home is one independent draw from `Y`, not one named `bldg_id`.

The search stops at the number of Eversource residential customers in that group. That cap is the group's share in the 2024 Residential Appliance Saturation Survey, Eversource column, times the Rate Year count of residential bills for Rates 1, 5, and 7. The shares and the bill count are the ones the notebook already uses: natural gas 29 percent, oil 39 percent, propane 7 percent, electrical resistance 12 percent (electric fuel minus primary heat pump), wood 3 percent. If the winter peak is still at or below the summer peak at that cap, the group does not flip the system.

Electrical resistance homes lower their winter grid use when they convert, so this group can widen the summer-over-winter gap. The notebook will say so when the search reaches the cap without a flip.

The two mixed orders in the notebook today (electric resistance first, then fossil fuel in proportion to the survey shares; fossil fuel first, then resistance; wood last in both) are not part of this calculation.

## How the percentile is evaluated

`Z_k` is defined as the k-fold convolution above. Writing that mixture down is possible for one home and impossible for the counts this question asks about. A cell's change sample has one point per building per hour of that cell, and k reaches the hundreds of thousands. `SumKDE`'s exact pairwise mixture is the definition for k = 1. It is not the evaluation method for the search.

For the search, the sum of k independent copies of `Y` is replaced by a normal with the same mean and variance as that sum. Both are analytic from the fitted KDE, the same moments `SumKDE.mean` and `SumKDE.var` use:

```text
mean of one home     = mean of the change sample
variance of one home = population variance of the change sample + (Scott bandwidth)^2
mean of k homes      = k × mean of one home
variance of k homes  = k × variance of one home
```

`Z_k` is then the system Gaussian mixture convolved with that normal. Each system component, centered on a scaled OCC-733 hour `x_i` with variance `h_X^2`, becomes a normal centered on `x_i + k × mean(Y)` with variance `h_X^2 + k × variance(Y)`. The percentile is the number q where the average of those normal cdfs equals `peak_quantile`. That inverse uses Brent's method, as `SumKDE.ppf` does. It has no Monte Carlo error.

The phrase "variance equal to the sum of the two bandwidths squared" is the width of one kernel in that mixture, `h_X^2 + h_Y^2` for a single home. It is not a new spread piled on top of the data, and it does not compound with the number of cells. `h_X` on the scaled system sample is 24 MW to 283 MW. A home's Scott bandwidth is a fraction of a kilowatt, so `h_Y^2` does not move `h_X` at the precision of a megawatt. Adding k homes adds k copies of the home's own variance. The standard deviation of that sum grows with the square root of k. At full conversion the notebook already puts the standard deviation of the added load between 0.1 MW and 2.3 MW, beside peaks of 3,256 MW in winter and 4,499 MW in summer and a gap of 1,243 MW. Pooling every hour, rather than one average per building, makes a single home's sample wider than that figure, and the aggregate standard deviation is still a few megawatts. The percentile moves with the mean of the added homes.

Two checks get computed and shown:

- At k = 1, this normal approximation of a single home against the exact `SumKDE` percentile, in every cell. The two should be close, and the comparison says how much of the one-home shape the normal drops.
- The k = 0 peaks, which are the exact percentiles of `X` at `peak_quantile` and do not use the normal approximation at all.

The search itself is a binary search on k when the winter-minus-summer gap is increasing in k, and a scan when it is not. The gap is increasing for a group whose winter cells pick up more load per home than its summer cells.

## What stays in the notebook, and what leaves the calculation

Stays, as the description of the inputs:

- The OCC-733 series, the yearly means, and the scale factors.
- The 576-cell labelling.
- The ResStock group counts and the upgrade-00 / upgrade-02 load files.
- The survey shares and the rate-year bill count, used only as the cap on k.
- The season definitions, June–September and December–February.

Leaves the calculation:

- Collapsing each building to its average kilowatt-hour in the cell before fitting.
- Moving each historical hour by the group's average change, and taking the highest moved hour as the peak.
- Averaging the four yearly peaks. The years are pooled into `X` after scaling, so there is one summer peak and one winter peak.
- The standard deviation of the independent-homes shift as a band around that average. The spread is inside `Z_k`, and the reported load is the `peak_quantile` percentile of `Z_k`.
- The comparison of paired and unpaired before/after home variances. The change sample is already the paired hourly difference. `SumKDE` adds the system density and the change density.
- The resistance-first and fossil-first paths, and the chart of those two paths.

The survey's cooling tables do not enter the peaks. Summer and winter both come from the upgrade-02 minus upgrade-00 electricity of the same buildings. The cooling writeup can stay as background or come out; it is not an input.

## Decisions to confirm

Edit this list in place. The rewrite will follow whatever is left here.

1. **One group at a time.** Each of natural gas, propane, oil, wood, and electrical resistance is added alone, starting from today's system. The heat-pump group is fit and not added. The mixed orders are dropped.
2. **Wood** is the ResStock `other` remainder. There is no wood flag to split out.
3. **The change sample is the paired hourly difference**, upgrade 02 minus upgrade 00, for every hour of every building in the cell. The density is fit to those differences. It is not a separate before density and after density added with `SumKDE`.
4. **The kernel is the untruncated Scott Gaussian** from `scipy.stats.gaussian_kde` on both sides. The truncated probability-of-peak kernel is not used.
5. **The cell value is the `peak_quantile` percentile of the summed density**, default `0.90`. One variable covers every cell, both seasons, and the crossing. The seasonal peak is the maximum of those cell values inside the season. Months stay June–September and December–February.
6. **A home is one draw from the group's change density**, in megawatts (`change_kwh / 1000`). Homes are unweighted. The search stops at survey share times rate-year residential bills.
7. **Many homes use the normal approximation** with the change KDE's own mean and variance, convolved with the exact system mixture. k = 1 is also reported with the exact `SumKDE` convolution.
