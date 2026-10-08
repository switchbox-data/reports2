"""Unit tests for two-block threshold personalization. No S3.

The personalized adjustment is checked two ways: against hand-worked dollar amounts for
each usage scenario, and against a brute-force rebuild of the monthly bill at both
thresholds across a grid of usage pairs. The rates are CT Eversource Rate 6 and its two
marginal-cost variants, delivery only, in $/kWh.
"""

from __future__ import annotations

import itertools

import polars as pl
import pytest

from lib.rates_analysis.block_rates import add_adjustment, month_block_rates, personalized_block_adjustment

THRESHOLD = 700.0
WINTER = ["Jan", "Feb", "Mar", "Nov", "Dec"]
SUMMER = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]

# (name, Block 1, Block 2). See rate-design-platform context/code/data/ct_eversource_custom_rates.md.
TARIFFS = [
    ("rate6", 0.13570, 0.11656),
    ("ratemc", 0.13570, 0.08291),
    ("fixed_ratemc", 0.09676, 0.04397),
]
TARIFF_IDS = [name for name, _r1, _r2 in TARIFFS]


def _schedule(period: int) -> list[int]:
    return [period] * 24


def _tariff(r1: float, r2: float, threshold: float = THRESHOLD) -> dict:
    """URDB-shaped two-block tariff: Nov-Mar two blocks at ``threshold``, Apr-Oct one block."""
    structure = [[{"rate": r1, "max": threshold}, {"rate": r2}], [{"rate": r1}]]
    winter_index = {0, 1, 2, 10, 11}
    schedule = [_schedule(0) if index in winter_index else _schedule(1) for index in range(12)]
    return {
        "energyratestructure": structure,
        "energyweekdayschedule": schedule,
        "energyweekendschedule": schedule,
    }


def _block_charge(kwh: float, r1: float, r2: float, threshold: float) -> float:
    """Energy charge for one two-block month, computed directly from the tariff definition."""
    return r1 * min(kwh, threshold) + r2 * max(kwh - threshold, 0.0)


def _expected(kwh_before: float, kwh_after: float, r1: float, r2: float) -> float:
    """Personalized minus filed charge for one winter month, by brute force."""
    filed = _block_charge(kwh_after, r1, r2, THRESHOLD)
    personalized = _block_charge(kwh_after, r1, r2, kwh_before)
    return personalized - filed


def _one_month(kwh_before: float, kwh_after: float, month: str = "Jan") -> pl.DataFrame:
    return pl.DataFrame({"bldg_id": [1], "month": [month], "kwh_before": [kwh_before], "kwh_after": [kwh_after]})


def _adjustment(kwh: pl.DataFrame, r1: float, r2: float) -> pl.DataFrame:
    return personalized_block_adjustment(kwh, month_block_rates(_tariff(r1, r2)))


# --- Reading the tariff -------------------------------------------------------------------


@pytest.mark.parametrize(("name", "r1", "r2"), TARIFFS, ids=TARIFF_IDS)
def test_month_block_rates_reads_real_rate6_structure(name: str, r1: float, r2: float) -> None:
    rates = month_block_rates(_tariff(r1, r2))

    assert rates["month"].to_list() == [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    winter = rates.filter(pl.col("month").is_in(WINTER))
    assert winter.height == 5
    assert winter["r1"].to_list() == pytest.approx([r1] * 5)
    assert winter["r2"].to_list() == pytest.approx([r2] * 5)
    assert winter["threshold_kwh"].to_list() == pytest.approx([THRESHOLD] * 5)
    summer = rates.filter(pl.col("month").is_in(SUMMER))
    assert summer.height == 7
    assert summer["r1"].to_list() == pytest.approx([r1] * 7)
    assert summer["r2"].null_count() == 7
    assert summer["threshold_kwh"].null_count() == 7


def test_month_block_rates_rejects_a_weekend_or_hourly_schedule() -> None:
    weekend = _tariff(0.10, 0.08)
    weekend["energyweekendschedule"] = [_schedule(1)] * 12
    with pytest.raises(ValueError, match="weekday and weekend"):
        month_block_rates(weekend)

    hourly = _tariff(0.10, 0.08)
    hourly["energyweekdayschedule"] = [[0] * 12 + [1] * 12] + [_schedule(1)] * 11
    hourly["energyweekendschedule"] = hourly["energyweekdayschedule"]
    with pytest.raises(ValueError, match="hour-flat"):
        month_block_rates(hourly)


def test_month_block_rates_rejects_more_than_two_blocks_or_a_missing_max() -> None:
    three = _tariff(0.10, 0.08)
    three["energyratestructure"][0] = [{"rate": 0.10, "max": 300}, {"rate": 0.09, "max": 700}, {"rate": 0.08}]
    with pytest.raises(ValueError, match="energy tiers"):
        month_block_rates(three)

    no_max = _tariff(0.10, 0.08)
    no_max["energyratestructure"][0] = [{"rate": 0.10}, {"rate": 0.08}]
    with pytest.raises(ValueError, match="kWh max"):
        month_block_rates(no_max)


def test_personalized_block_adjustment_requires_the_kwh_columns() -> None:
    rates = month_block_rates(_tariff(0.10, 0.08))
    with pytest.raises(ValueError, match="kwh_after"):
        personalized_block_adjustment(pl.DataFrame({"bldg_id": [1], "month": ["Jan"], "kwh_before": [1.0]}), rates)


# --- One winter month, hand-worked -----------------------------------------------------------
#
# A gas home on Rate 6 that used 441 kWh in January and uses 1,349 kWh after the heat pump
# is the typical case from the CT analysis. Each scenario below says what the filed and
# personalized tariffs charge and why they differ.


@pytest.mark.parametrize(("name", "r1", "r2"), TARIFFS, ids=TARIFF_IDS)
class TestOneWinterMonth:
    def test_typical_gas_home_gets_the_block_gap_on_kwh_between_old_usage_and_700(
        self, name: str, r1: float, r2: float
    ) -> None:
        # Filed: 700 at r1, 649 at r2. Personalized: 441 at r1, 908 at r2.
        # The 259 kWh between 441 and 700 move from r1 to r2.
        result = _adjustment(_one_month(441.0, 1349.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r2 - r1) * (700.0 - 441.0))
        assert result["adjustment"].item() == pytest.approx(_expected(441.0, 1349.0, r1, r2))

    def test_load_decrease_from_above_700_pays_more_on_kwh_still_above_700(
        self, name: str, r1: float, r2: float
    ) -> None:
        # 2,104 -> 1,024 is the electric-resistance case. Under the personalized threshold
        # the whole 1,024 kWh is below the home's own 2,104, so it all pays r1. Under the
        # filed threshold 324 kWh paid r2, so the home pays more.
        result = _adjustment(_one_month(2104.0, 1024.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r1 - r2) * (1024.0 - 700.0))
        assert result["adjustment"].item() == pytest.approx(_expected(2104.0, 1024.0, r1, r2))

    def test_load_decrease_that_ends_below_700_changes_nothing(self, name: str, r1: float, r2: float) -> None:
        # Both tariffs charge r1 on every kWh when usage ends below 700 and below the old usage.
        result = _adjustment(_one_month(900.0, 500.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx(0.0)

    def test_unchanged_load_below_700_changes_nothing(self, name: str, r1: float, r2: float) -> None:
        result = _adjustment(_one_month(500.0, 500.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx(0.0)

    def test_unchanged_load_above_700_pays_more(self, name: str, r1: float, r2: float) -> None:
        # Filed gave r2 on the 300 kWh above 700. Personalized sets the threshold at the
        # home's own 1,000, so no kWh is above it and everything pays r1.
        result = _adjustment(_one_month(1000.0, 1000.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r1 - r2) * 300.0)
        assert result["adjustment"].item() == pytest.approx(_expected(1000.0, 1000.0, r1, r2))

    def test_increase_that_stays_below_700_still_gets_the_discount(self, name: str, r1: float, r2: float) -> None:
        # 300 -> 500. Filed charges r1 on all 500. Personalized charges r1 on 300 and r2 on
        # the 200 kWh of growth. The filed threshold never comes into it.
        result = _adjustment(_one_month(300.0, 500.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r2 - r1) * 200.0)
        assert result["adjustment"].item() == pytest.approx(_expected(300.0, 500.0, r1, r2))

    def test_increase_that_lands_exactly_on_700(self, name: str, r1: float, r2: float) -> None:
        # Filed charges r1 on all 700. Personalized: r1 on 450, r2 on 250.
        result = _adjustment(_one_month(450.0, 700.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r2 - r1) * 250.0)

    def test_increase_from_above_700_pays_more_on_the_old_usage_above_700(
        self, name: str, r1: float, r2: float
    ) -> None:
        # 900 -> 1,500. Filed: r2 on 800. Personalized: r2 on 600. The 200 kWh between 700
        # and the old 900 move back to r1.
        result = _adjustment(_one_month(900.0, 1500.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r1 - r2) * 200.0)
        assert result["adjustment"].item() == pytest.approx(_expected(900.0, 1500.0, r1, r2))

    def test_zero_usage_before_gets_the_discount_on_every_kwh_up_to_700(self, name: str, r1: float, r2: float) -> None:
        # Filed: r1 on 700, r2 on 300. Personalized threshold is 0, so r2 on all 1,000.
        result = _adjustment(_one_month(0.0, 1000.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx((r2 - r1) * 700.0)

    def test_zero_usage_after_changes_nothing(self, name: str, r1: float, r2: float) -> None:
        result = _adjustment(_one_month(400.0, 0.0), r1, r2)
        assert result["adjustment"].item() == pytest.approx(0.0)

    def test_summer_month_is_dropped_even_when_usage_rises(self, name: str, r1: float, r2: float) -> None:
        result = _adjustment(_one_month(300.0, 2000.0, month="Jul"), r1, r2)
        assert result.height == 0


# --- Brute-force grid --------------------------------------------------------------------------


@pytest.mark.parametrize(("name", "r1", "r2"), TARIFFS, ids=TARIFF_IDS)
def test_formula_matches_bill_rebuild_across_a_usage_grid(name: str, r1: float, r2: float) -> None:
    usage = [0.0, 1.0, 100.0, 441.0, 699.0, 700.0, 701.0, 900.0, 1349.0, 2104.0, 3000.0, 5000.0]
    pairs = list(itertools.product(usage, usage))
    kwh = pl.DataFrame(
        {
            "bldg_id": list(range(len(pairs))),
            "month": ["Jan"] * len(pairs),
            "kwh_before": [before for before, _after in pairs],
            "kwh_after": [after for _before, after in pairs],
        }
    )

    result = _adjustment(kwh, r1, r2).sort("bldg_id")

    assert result.height == len(pairs)
    expected = [_expected(before, after, r1, r2) for before, after in pairs]
    assert result["adjustment"].to_list() == pytest.approx(expected, abs=1e-9)


def test_formula_matches_bill_rebuild_for_an_arbitrary_threshold() -> None:
    # Nothing in the math assumes 700 kWh.
    r1, r2, threshold = 0.20, 0.05, 1200.0
    rates = month_block_rates(_tariff(r1, r2, threshold))
    kwh = pl.DataFrame(
        {
            "bldg_id": [1, 2, 3, 4],
            "month": ["Jan"] * 4,
            "kwh_before": [500.0, 1500.0, 1200.0, 1300.0],
            "kwh_after": [2000.0, 2000.0, 1200.0, 1250.0],
        }
    )

    result = personalized_block_adjustment(kwh, rates).sort("bldg_id")

    expected = [
        _block_charge(after, r1, r2, before) - _block_charge(after, r1, r2, threshold)
        for before, after in zip(kwh["kwh_before"], kwh["kwh_after"], strict=True)
    ]
    assert result["adjustment"].to_list() == pytest.approx(expected)
    assert expected[0] == pytest.approx((r2 - r1) * 700.0)
    assert expected[1] == pytest.approx((r1 - r2) * 300.0)
    assert expected[2] == pytest.approx(0.0)
    assert expected[3] == pytest.approx((r1 - r2) * 50.0)


# --- Across the three tariffs -----------------------------------------------------------------


def test_ratemc_and_fixed_ratemc_have_the_same_block_gap_and_the_same_adjustment() -> None:
    kwh = _one_month(441.0, 1349.0)
    ratemc = _adjustment(kwh, 0.13570, 0.08291)["adjustment"].item()
    fixed = _adjustment(kwh, 0.09676, 0.04397)["adjustment"].item()
    rate6 = _adjustment(kwh, 0.13570, 0.11656)["adjustment"].item()

    assert ratemc == pytest.approx(fixed)
    assert ratemc == pytest.approx(-0.05279 * 259.0)
    assert rate6 == pytest.approx(-0.01914 * 259.0)
    assert abs(ratemc) > abs(rate6)


@pytest.mark.parametrize(
    ("name", "r1", "r2", "ceiling"),
    [
        ("rate6", 0.13570, 0.11656, 0.01914 * 700.0 * 5),
        ("ratemc", 0.13570, 0.08291, 0.05279 * 700.0 * 5),
        ("fixed_ratemc", 0.09676, 0.04397, 0.05279 * 700.0 * 5),
    ],
    ids=TARIFF_IDS,
)
def test_annual_saving_is_capped_at_gap_times_700_times_five_months(
    name: str, r1: float, r2: float, ceiling: float
) -> None:
    # Zero usage before, at least 700 after, in every winter month, is the most any home
    # can gain. Using far more than 700 kWh after does not add to it.
    kwh = pl.DataFrame(
        {
            "bldg_id": [1] * 12,
            "month": WINTER + SUMMER,
            "kwh_before": [0.0] * 12,
            "kwh_after": [700.0, 5000.0, 10000.0, 700.0, 999.0] + [5000.0] * 7,
        }
    )

    annual = _adjustment(kwh, r1, r2).group_by("bldg_id").agg(pl.col("adjustment").sum())

    assert annual["adjustment"].item() == pytest.approx(-ceiling)
    assert ceiling == pytest.approx({"rate6": 66.99, "ratemc": 184.765, "fixed_ratemc": 184.765}[name])


# --- Twelve months and the bill-change frame ---------------------------------------------------


def test_annual_adjustment_sums_winter_months_only() -> None:
    r1, r2 = 0.13570, 0.11656
    before = {"Jan": 441.0, "Feb": 400.0, "Mar": 350.0, "Nov": 300.0, "Dec": 800.0}
    after = {"Jan": 1349.0, "Feb": 1200.0, "Mar": 900.0, "Nov": 650.0, "Dec": 700.0}
    months = WINTER + SUMMER
    kwh = pl.DataFrame(
        {
            "bldg_id": [1] * 12,
            "month": months,
            "kwh_before": [before.get(month, 300.0) for month in months],
            "kwh_after": [after.get(month, 3000.0) for month in months],
        }
    )

    monthly = _adjustment(kwh, r1, r2)

    assert sorted(monthly["month"].to_list()) == sorted(WINTER)
    by_month = dict(zip(monthly["month"], monthly["adjustment"], strict=True))
    assert by_month["Jan"] == pytest.approx((r2 - r1) * 259.0)
    assert by_month["Feb"] == pytest.approx((r2 - r1) * 300.0)
    assert by_month["Mar"] == pytest.approx((r2 - r1) * 350.0)
    assert by_month["Nov"] == pytest.approx((r2 - r1) * 350.0)  # stays below 700: all 350 kWh of growth
    assert by_month["Dec"] == pytest.approx(0.0)  # usage fell to 700: every kWh at r1 either way
    expected_annual = sum(_expected(before[month], after[month], r1, r2) for month in WINTER)
    assert monthly["adjustment"].sum() == pytest.approx(expected_annual)


def test_personalized_bill_equals_a_bill_rebuilt_at_the_personal_threshold() -> None:
    """Rebuilding the whole annual bill both ways gives the same answer as 700 kWh bill + adjustment."""
    r1, r2 = 0.13570, 0.08291
    fixed_monthly = 30.95
    rates = month_block_rates(_tariff(r1, r2))
    months = WINTER + SUMMER
    homes = {
        1: ([441.0] * 5 + [300.0] * 7, [1349.0] * 5 + [500.0] * 7),  # gas home
        2: ([2104.0] * 5 + [600.0] * 7, [1024.0] * 5 + [900.0] * 7),  # electric resistance
        3: ([650.0] * 5 + [400.0] * 7, [690.0] * 5 + [400.0] * 7),  # small increase, stays below 700
    }
    kwh = pl.DataFrame(
        {
            "bldg_id": [bldg for bldg, (b, _a) in homes.items() for _ in b],
            "month": months * len(homes),
            "kwh_before": [x for _bldg, (b, _a) in homes.items() for x in b],
            "kwh_after": [x for _bldg, (_b, a) in homes.items() for x in a],
        }
    )

    def annual_bill(threshold_by_month: dict[str, float], usage: list[float]) -> float:
        total = fixed_monthly * 12
        for month, used in zip(months, usage, strict=True):
            threshold = threshold_by_month.get(month)
            total += r1 * used if threshold is None else _block_charge(used, r1, r2, threshold)
        return total

    filed = {bldg: annual_bill(dict.fromkeys(WINTER, THRESHOLD), a) for bldg, (_b, a) in homes.items()}
    personal = {
        bldg: annual_bill({month: b[months.index(month)] for month in WINTER}, a) for bldg, (b, a) in homes.items()
    }
    frame = pl.DataFrame(
        {"bldg_id": list(homes), "bill_after": [filed[bldg] for bldg in homes], "delta": [0.0] * len(homes)}
    )
    annual_adjustment = personalized_block_adjustment(kwh, rates).group_by("bldg_id").agg(pl.col("adjustment").sum())

    shifted = add_adjustment(frame, annual_adjustment, ["bill_after", "delta"]).sort("bldg_id")

    assert shifted["bill_after"].to_list() == pytest.approx([personal[bldg] for bldg in homes])
    assert shifted["delta"].to_list() == pytest.approx([personal[bldg] - filed[bldg] for bldg in homes])
    assert shifted["delta"][0] < 0  # gas home saves
    assert shifted["delta"][1] > 0  # electric resistance pays more
    assert shifted["delta"][2] == pytest.approx((r2 - r1) * 40.0 * 5)  # below-700 growth still discounted


def test_add_adjustment_inner_requires_every_building_and_left_fills_zero() -> None:
    frame = pl.DataFrame({"bldg_id": [1, 2], "delta": [10.0, 20.0], "bill_after": [100.0, 200.0]})
    adjustment = pl.DataFrame({"bldg_id": [1], "adjustment": [-3.0]})

    shifted = add_adjustment(frame.filter(pl.col("bldg_id") == 1), adjustment, ["delta", "bill_after"])
    assert shifted["delta"].item() == pytest.approx(7.0)
    assert shifted["bill_after"].item() == pytest.approx(97.0)

    with pytest.raises(ValueError, match="row count"):
        add_adjustment(frame, adjustment, ["delta"])

    filled = add_adjustment(frame, adjustment, ["delta"], how="left")
    assert filled.sort("bldg_id")["delta"].to_list() == pytest.approx([7.0, 20.0])


def test_add_adjustment_rejects_duplicate_adjustment_rows() -> None:
    frame = pl.DataFrame({"bldg_id": [1], "delta": [10.0]})
    duplicated = pl.DataFrame({"bldg_id": [1, 1], "adjustment": [-3.0, -4.0]})
    with pytest.raises(ValueError, match="row count"):
        add_adjustment(frame, duplicated, ["delta"])
