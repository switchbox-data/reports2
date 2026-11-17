"""Remove the files of scenarios no longer in SCENARIOS from the public CIEC-11(c) folder.

The kept set is what ``publish_ciec_11c_share.py`` would upload today: the outputs of the runs in
``build_ciec_11c_share.SCENARIOS``, and the inputs, less the electric tariffs and tariff maps that
only the dropped runs read. Rewrites MANIFEST.csv and staged_inputs.csv to match and uploads the
manifest. Dry run by default; pass ``--execute`` to delete.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import boto3
from build_ciec_11c_share import PATH_CT_CONFIG, RUNS, Stager, repo_relative
from publish_ciec_11c_share import DEST_BUCKET, DEST_PREFIX, output_objects, put_file

PATH_REPORT = Path(__file__).resolve().parent.parent
ELECTRIC_CONFIG = ("inputs/config/tariffs/electric/", "inputs/config/tariff_maps/electric/")
SITE_FILES = {"MANIFEST.csv", "README.md"}


def kept_electric_config(stager: Stager) -> set[str]:
    """Public paths of the electric tariffs and tariff maps the kept runs read."""
    paths = set()
    for run in RUNS:
        s = stager.run_json(run, "scenario_settings.json")
        repo_paths = [repo_relative(p) for p in s["path_tariffs_electric"].values()]
        repo_paths.append(repo_relative(s["path_tariff_maps_electric"]))
        paths.update(f"inputs/config/{p.removeprefix(PATH_CT_CONFIG)}" for p in repo_paths)
    return paths


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open() as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--path-staged-dir", type=Path, default=PATH_REPORT / "cache" / "ciec_11c_share")
    parser.add_argument("--execute", action="store_true", help="delete (default: dry run)")
    args = parser.parse_args()

    stager = Stager(args.path_staged_dir)
    keep_outputs = {public for _, public, _ in output_objects()}
    keep_config = kept_electric_config(stager)

    def keep(path: str) -> bool:
        if path.startswith("outputs/"):
            return path in keep_outputs
        if path.startswith(ELECTRIC_CONFIG):
            return path in keep_config
        return True

    path_manifest = args.path_staged_dir / "MANIFEST.csv"
    fields, manifest = read_csv(path_manifest)
    kept = [r for r in manifest if keep(r["path"])]
    dropped = [r["path"] for r in manifest if not keep(r["path"])]
    assert keep_outputs <= {r["path"] for r in kept}, "a kept output is missing from the manifest"
    assert keep_config <= {r["path"] for r in kept}, "a kept tariff is missing from the manifest"

    for path in dropped:
        print(f"  remove {path}")
    print(f"{len(dropped)} files to remove; {len(kept)} remain")
    if not args.execute:
        print("Dry run; pass --execute to delete.")
        return

    s3 = boto3.client("s3", region_name="us-west-2")
    for i in range(0, len(dropped), 1000):
        batch = [{"Key": f"{DEST_PREFIX}/{p}"} for p in dropped[i : i + 1000]]
        result = s3.delete_objects(Bucket=DEST_BUCKET, Delete={"Objects": batch, "Quiet": True})
        assert not result.get("Errors"), result["Errors"]

    write_csv(path_manifest, fields, kept)
    put_file(s3, path_manifest, "MANIFEST.csv")

    path_staged = args.path_staged_dir / "staged_inputs.csv"
    staged_fields, staged = read_csv(path_staged)
    for row in staged:
        if not keep(row["path"]):
            (args.path_staged_dir / row["path"]).unlink()
    write_csv(path_staged, staged_fields, [r for r in staged if keep(r["path"])])

    listed = {
        obj["Key"].removeprefix(f"{DEST_PREFIX}/")
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=DEST_BUCKET, Prefix=f"{DEST_PREFIX}/")
        for obj in page.get("Contents", [])
    }
    expected = {r["path"] for r in kept}
    assert listed - SITE_FILES == expected, f"extra {listed - SITE_FILES - expected}, missing {expected - listed}"
    print(f"Removed {len(dropped)} files; the folder matches MANIFEST.csv ({len(kept)} files).")


if __name__ == "__main__":
    main()
