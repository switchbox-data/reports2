"""Generic S3 helpers for listing directories and resolving run paths."""

from __future__ import annotations

import boto3


def list_s3_subdirs(s3_prefix: str) -> list[str]:
    """Return immediate subdirectory paths under *s3_prefix*.

    Example: given ``s3://bucket/path/batch/``, returns a list of
    ``s3://bucket/path/batch/<subdir>`` strings.
    """
    bucket, key = s3_prefix.replace("s3://", "").split("/", 1)
    prefix = key.rstrip("/") + "/"
    out: list[str] = []
    paginator = boto3.client("s3").get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for entry in page.get("CommonPrefixes", []):
            out.append(f"s3://{bucket}/{entry['Prefix'].rstrip('/')}")
    return out


def run_dir(subdirs: list[str], name_ends_with: str) -> str:
    """Find exactly one subdir whose leaf name ends with *name_ends_with*."""
    matches = [d for d in subdirs if d.rstrip("/").split("/")[-1].endswith(name_ends_with)]
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one subdir ending with {name_ends_with!r}; got {len(matches)}")
    return matches[0]
