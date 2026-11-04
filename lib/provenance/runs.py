"""Internal checks of the CAIRO runs behind a testimony (written to the review CSV only).

Confirms that every run in the batch recorded its settings and marginal-cost files, that the
tariff and tariff-map files it read exist at the pinned rate-design-platform commit, that
the pinned tariffs match what CAIRO ran, and that the marginal-cost files on S3 still hash
to what the runs used.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from lib.provenance.resolve import git, git_show
from lib.provenance.review import Review, flag

S3_BUCKET = "data.sb"


def _s3_json(s3: Any, bucket: str, key: str) -> Any:
    try:
        return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    except s3.exceptions.NoSuchKey:
        return None


def _urdb_rates(urdb: dict[str, Any]) -> tuple[float, list[float]]:
    item = urdb["items"][0]
    rates = sorted(
        round(t.get("rate", 0.0) + t.get("adj", 0.0), 8) for period in item["energyratestructure"] for t in period
    )
    return float(item.get("fixedchargefirstmeter", 0.0)), rates


def _cairo_rates(cfg: dict[str, Any]) -> tuple[float, list[float]]:
    return float(cfg["ur_monthly_fixed_charge"]), sorted(round(row[4], 8) for row in cfg["ur_ec_tou_mat"])


def _iter_mc_records(used: Any, mc_types: set[str]) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []

    def walk(node: Any, mc_type: str | None) -> None:
        if isinstance(node, dict):
            if "sha256" in node and "path" in node and str(node["path"]).startswith("s3://"):
                out.append((mc_type or "?", node))
                return
            for k, v in node.items():
                walk(v, mc_type or (k if k in mc_types else None))
        elif isinstance(node, list):
            for v in node:
                walk(v, mc_type)

    walk(used, None)
    return [(t, r) for t, r in out if t in mc_types]


def _rdp_rel(local_path: str | None) -> str | None:
    if not local_path:
        return None
    m = re.search(r"rate-design-platform/(.+)$", local_path)
    return m.group(1) if m else None


def _rdp_exists(path_rdp: Path, rdp_pin: str, rel: str) -> bool:
    return git(path_rdp, "cat-file", "-e", f"{rdp_pin}:{rel}", check=False).returncode == 0


def _precalc_uncalibrated(run_name: str) -> bool:
    return "_precalc_" in run_name and "uncalibrated" in run_name


def check_runs(
    review: Review,
    *,
    batch_prefix: str,
    path_rdp: Path,
    rdp_pin: str,
    mc_types: Iterable[str],
    compare_tariffs: Callable[[str], bool] = _precalc_uncalibrated,
    bucket: str = S3_BUCKET,
) -> None:
    """``compare_tariffs(run_name)`` picks the runs whose CAIRO tariffs are compared to the pin."""
    import boto3

    mc_set = set(mc_types)
    s3 = boto3.client("s3")
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=batch_prefix, Delimiter="/")
    runs = [
        p["Prefix"]
        for page in pages
        for p in page.get("CommonPrefixes", [])
        if re.search(r"/\d{8}_\d{6}_[^/]+/$", p["Prefix"])
    ]
    n_tariffs = 0
    mc_seen: dict[str, set[str]] = defaultdict(set)
    mc_paths: dict[str, str] = {}
    # Older runs predate marginal_costs_used.json; their settings still name the MC files.
    mc_unhashed: dict[str, set[str]] = defaultdict(set)
    first_run_time: datetime | None = None
    for run in runs:
        run_name = run.rstrip("/").rsplit("/", 1)[-1]
        run_time = datetime.strptime(run_name[:15], "%Y%m%d_%H%M%S").replace(tzinfo=UTC)
        first_run_time = min(first_run_time or run_time, run_time)
        settings = _s3_json(s3, bucket, run + "scenario_settings.json")
        if settings is None:
            flag(review, "run_record_missing", run_name, "no scenario_settings.json")
            continue
        used = _s3_json(s3, bucket, run + "marginal_costs_used.json")
        if used is None:
            for mc_type in mc_set:
                if path := settings.get(f"path_{mc_type}_mc"):
                    mc_unhashed[mc_type].add(path)
        else:
            for mc_type, rec in _iter_mc_records(used, mc_set):
                mc_seen[mc_type].add(rec["sha256"])
                mc_paths[mc_type] = rec["path"]
        for path_key in ("path_tariff_maps_electric", "path_tariff_maps_gas"):
            rel = _rdp_rel(settings.get(path_key))
            if rel and not _rdp_exists(path_rdp, rdp_pin, rel):
                flag(review, "run_file_missing", run_name, f"{rel} not at {rdp_pin}")
        if not compare_tariffs(run_name):
            continue
        final = _s3_json(s3, bucket, run + "tariff_final_config.json") or {}
        for key, local_path in settings.get("path_tariffs_electric", {}).items():
            rel = _rdp_rel(local_path)
            if not rel or not _rdp_exists(path_rdp, rdp_pin, rel):
                flag(review, "run_file_missing", run_name, f"{rel} not at {rdp_pin}")
                continue
            if key not in final:
                continue
            pinned = _urdb_rates(json.loads(git_show(rdp_pin, rel, path_rdp)))
            ran = _cairo_rates(final[key])
            n_tariffs += 1
            if abs(pinned[0] - ran[0]) > 1e-6 or pinned[1] != ran[1]:
                flag(review, "run_tariff_vs_pin", run_name, f"{rel}: pinned fixed/rates {pinned} vs run {ran}")
    for mc_type, hashes in mc_seen.items():
        if len(hashes) != 1:
            flag(review, "mc_hash", mc_type, f"runs used {len(hashes)} different files")
            continue
        path = mc_paths[mc_type]
        b, key = path.removeprefix("s3://").split("/", 1)
        live = hashlib.sha256(s3.get_object(Bucket=b, Key=key)["Body"].read()).hexdigest()
        if live != next(iter(hashes)):
            flag(review, "mc_hash", mc_type, f"live {live} vs run {next(iter(hashes))}")
    for mc_type, paths in sorted(mc_unhashed.items()):
        if len(paths) != 1:
            flag(review, "mc_unrecorded", mc_type, f"runs read {sorted(paths)}")
            continue
        path = next(iter(paths))
        b, key = path.removeprefix("s3://").split("/", 1)
        head = s3.head_object(Bucket=b, Key=key)
        modified: datetime = head["LastModified"]
        sha = hashlib.sha256(s3.get_object(Bucket=b, Key=key)["Body"].read()).hexdigest()
        unchanged = first_run_time is not None and modified < first_run_time
        flag(
            review,
            "mc_unrecorded" if not unchanged else "mc_unchanged_since_runs",
            mc_type,
            f"{path} (no run hash record); last modified {modified.isoformat()}, "
            f"first run {first_run_time.isoformat() if first_run_time else '?'}; sha256 {sha[:12]}",
        )
    flag(
        review,
        "runs_checked",
        str(len(runs)),
        f"run directories; {n_tariffs} precalc tariffs compared to {rdp_pin}; "
        f"MC files hashed: {sorted(mc_seen)}; MC files dated: {sorted(mc_unhashed)}",
    )
