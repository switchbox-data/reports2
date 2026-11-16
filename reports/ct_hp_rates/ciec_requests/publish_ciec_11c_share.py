"""Upload the CIEC-11(c) files to the public bucket, with MANIFEST.csv and README.md.

Outputs are copied server-side from ``data.sb`` unchanged; inputs are the files staged by
``build_ciec_11c_share.py``. Every object's SHA-256 is checked by S3 against our own hash.

Dry run by default: checks that every source exists and that the bucket is still private,
then prints what would be uploaded. Pass ``--execute`` to upload.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
from pathlib import Path

import boto3
from build_ciec_11c_share import BATCH_PREFIX, BUCKET, RUNS, SCENARIOS, UTILITY, sha256

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parent

DEST_BUCKET = "switchbox-public-data"
DEST_PREFIX = "ct_hp_rates/pura_26-05-10/ciec-11c"
URL_BASE = f"https://{DEST_BUCKET}.s3.us-west-2.amazonaws.com/{DEST_PREFIX}"
MASTER_PREFIX = "switchbox/cairo/outputs/hp_rates/ct/all_utilities/ct_20261015_a"
MASTER_TABLES = {
    "comb_bills_year_target": "Customer bills by month and year",
    "cross_subsidization_BAT_values": "Customer bill alignment results",
}
RUN_FILES = {
    "tariff_final_config.json": "Tariff billed by the run",
    "scenario_settings.json": "Run settings",
    "marginal_costs_used.json": "Marginal cost files read by the run",
}
HOURLY_RUNS = {RUNS[0], RUNS[2]}  # Rate 1 precalc and calibrated delivery runs
CONTENT_TYPES = {
    ".parquet": "application/vnd.apache.parquet",
    ".json": "application/json",
    ".csv": "text/csv; charset=utf-8",
    ".yaml": "application/yaml",
    ".md": "text/markdown; charset=utf-8",
}


def content_type(key: str) -> str:
    return CONTENT_TYPES[Path(key).suffix]


def b64(hex_digest: str) -> str:
    return base64.b64encode(bytes.fromhex(hex_digest)).decode()


def output_objects() -> list[tuple[str, str, str]]:
    """(source key in data.sb, public path, description) for every output."""
    objects = []
    for scenario in SCENARIOS:
        for stage in ("precalc", "calibrated"):
            segment = f"default_ry1_{scenario}_uncalibrated_{stage}"
            for table, description in MASTER_TABLES.items():
                rel = f"{segment}/{table}/sb.electric_utility={UTILITY}/data.parquet"
                objects.append((f"{MASTER_PREFIX}/{rel}", f"outputs/master/{rel}", f"{description}, {segment}"))
    for run in RUNS:
        files = dict(RUN_FILES)
        if run.endswith("_delivery"):  # supply runs don't write billed kWh
            files["billing_kwh_annual.parquet"] = "Annual billed kWh per customer"
        if run in HOURLY_RUNS:
            files["billing_kwh_8760.parquet"] = "Hourly billed kWh per customer (timestamps UTC)"
        for name, description in files.items():
            objects.append((f"{BATCH_PREFIX}/{run}/{name}", f"outputs/runs/{run}/{name}", description))
    return objects


def check_private(s3) -> None:
    """Refuse to upload unless the bucket is still closed to the public."""
    block = s3.get_public_access_block(Bucket=DEST_BUCKET)["PublicAccessBlockConfiguration"]
    assert all(block.values()), f"{DEST_BUCKET} public access block is not fully on: {block}"
    try:
        s3.get_bucket_policy(Bucket=DEST_BUCKET)
    except s3.exceptions.ClientError as e:
        assert e.response["Error"]["Code"] == "NoSuchBucketPolicy", e
    else:
        raise AssertionError(f"{DEST_BUCKET} has a bucket policy; run `just ciec-11c-bucket close` first")


def copy_output(s3, src_key: str, public_path: str) -> str:
    """Server-side copy; S3's SHA-256 of the copy must equal ours of the source."""
    h = hashlib.sha256()
    for block in s3.get_object(Bucket=BUCKET, Key=src_key)["Body"].iter_chunks(1 << 20):
        h.update(block)
    digest = h.hexdigest()
    result = s3.copy_object(
        Bucket=DEST_BUCKET,
        Key=f"{DEST_PREFIX}/{public_path}",
        CopySource={"Bucket": BUCKET, "Key": src_key},
        MetadataDirective="REPLACE",
        ContentType=content_type(public_path),
        ServerSideEncryption="AES256",
        ChecksumAlgorithm="SHA256",
    )
    assert result["CopyObjectResult"]["ChecksumSHA256"] == b64(digest), f"checksum mismatch: {public_path}"
    return digest


def put_file(s3, path: Path, public_path: str) -> str:
    """Single-part upload; S3 rejects it if the bytes don't match our SHA-256."""
    digest = sha256(path)
    with path.open("rb") as f:
        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=f"{DEST_PREFIX}/{public_path}",
            Body=f,
            ContentType=content_type(public_path),
            ServerSideEncryption="AES256",
            ChecksumSHA256=b64(digest),
        )
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--path-staged-dir", type=Path, default=PATH_REPORT / "cache" / "ciec_11c_share")
    parser.add_argument("--path-readme", type=Path, default=PATH_HERE / "ciec_11c_README.md")
    parser.add_argument("--execute", action="store_true", help="upload (default: dry run)")
    args = parser.parse_args()

    s3 = boto3.client("s3", region_name="us-west-2")
    check_private(s3)

    outputs = output_objects()
    sizes = {src: s3.head_object(Bucket=BUCKET, Key=src)["ContentLength"] for src, _, _ in outputs}
    with (args.path_staged_dir / "staged_inputs.csv").open() as f:
        inputs = list(csv.DictReader(f))
    for row in inputs:
        assert (args.path_staged_dir / row["path"]).stat().st_size == int(row["bytes"]), row["path"]
    assert args.path_readme.exists(), args.path_readme

    n_bytes = sum(sizes.values()) + sum(int(r["bytes"]) for r in inputs)
    print(f"{len(outputs)} outputs + {len(inputs)} inputs, {n_bytes / 1e9:.2f} GB -> s3://{DEST_BUCKET}/{DEST_PREFIX}/")
    if not args.execute:
        print("Dry run; pass --execute to upload.")
        return

    manifest = []
    for i, (src, public_path, description) in enumerate(outputs, 1):
        digest = copy_output(s3, src, public_path)
        manifest.append((public_path, sizes[src], digest, description))
        print(f"  [{i}/{len(outputs)}] {public_path}")
    for row in inputs:
        digest = put_file(s3, args.path_staged_dir / row["path"], row["path"])
        assert digest == row["sha256"], f"staged file changed since staging: {row['path']}"
        manifest.append((row["path"], int(row["bytes"]), digest, row["description"]))
        print(f"  {row['path']}")

    path_manifest = args.path_staged_dir / "MANIFEST.csv"
    with path_manifest.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "bytes", "sha256", "description", "url"])
        for public_path, size, digest, description in sorted(manifest):
            writer.writerow([public_path, size, digest, description, f"{URL_BASE}/{public_path}"])
    put_file(s3, path_manifest, "MANIFEST.csv")
    put_file(s3, args.path_readme, "README.md")

    listed = {
        obj["Key"].removeprefix(f"{DEST_PREFIX}/")
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=DEST_BUCKET, Prefix=f"{DEST_PREFIX}/")
        for obj in page.get("Contents", [])
    }
    expected = {p for p, *_ in manifest} | {"MANIFEST.csv", "README.md"}
    assert listed == expected, f"bucket differs from manifest: extra {listed - expected}, missing {expected - listed}"
    print(f"Uploaded {len(expected)} objects; bucket contents match MANIFEST.csv. The bucket is still private.")


if __name__ == "__main__":
    main()
