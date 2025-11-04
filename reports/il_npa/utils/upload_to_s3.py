#!/usr/bin/env python3
"""
Upload People's Gas GeoJSON to public S3 bucket.

Uploads the peoplesgas_projects.geojson file to:
  s3://data.sb/gis/pgl/peoplesgas_projects.geojson

Requires AWS credentials configured in ~/.aws/credentials or environment variables.
"""

import os
from datetime import UTC, datetime
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def upload_to_s3(
    local_file: str | Path,
    bucket: str = "data.sb",
    s3_key: str = "gis/pgl/peoplesgas_projects.geojson",
) -> bool:
    """
    Upload a file to an S3 bucket.

    Args:
        local_file: Path to file to upload
        bucket: S3 bucket name
        s3_key: S3 object key (path within bucket)

    Returns:
        True if upload was successful, False otherwise

    Note:
        Public access is controlled by the bucket policy, not ACLs.
    """
    local_file = Path(local_file)

    if not local_file.exists():
        print(f"❌ Error: File not found: {local_file}")
        return False

    file_size_mb = local_file.stat().st_size / (1024 * 1024)

    print("=" * 70)
    print("📤 Uploading to AWS S3")
    print("=" * 70)
    print(f"Local file:  {local_file}")
    print(f"File size:   {file_size_mb:.2f} MB")
    print(f"Bucket:      {bucket}")
    print(f"S3 key:      {s3_key}")
    print()

    try:
        # Create S3 client
        s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))

        # Extra arguments for the upload
        extra_args = {
            "ContentType": "application/geo+json",
            "Metadata": {
                "uploaded_at": datetime.now(UTC).isoformat(),
                "source": "peoples_gas_arcgis",
            },
        }

        # Note: ACL is not set because the bucket uses "Bucket owner enforced" ownership
        # Public access should be configured via bucket policy instead

        # Upload the file
        print("⬆️  Uploading...")
        s3_client.upload_file(str(local_file), bucket, s3_key, ExtraArgs=extra_args)

        # Generate the public URL
        s3_url = f"https://{bucket}.s3.{s3_client.meta.region_name}.amazonaws.com/{s3_key}"

        print("✅ Upload successful!")
        print()
        print("🌐 Public URL:")
        print(f"   {s3_url}")
        print()
        print("📍 S3 URI:")
        print(f"   s3://{bucket}/{s3_key}")
        print()
        print("🗺️  View in geojson.io:")
        print(f"   http://geojson.io/#data=data:text/x-url,{s3_url}")
        print("=" * 70)

        return True

    except NoCredentialsError:
        print("❌ Error: AWS credentials not found")
        print("   Make sure your ~/.aws/credentials file is configured")
        print("   or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        return False

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_msg = e.response.get("Error", {}).get("Message", str(e))
        print(f"❌ AWS Error ({error_code}): {error_msg}")

        if error_code == "NoSuchBucket":
            print(f"   The bucket '{bucket}' does not exist or you don't have access to it")
        elif error_code == "AccessDenied":
            print(f"   Access denied. Check your AWS permissions for bucket '{bucket}'")

        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return False


def find_latest_geojson(directory: Path) -> Path | None:
    """
    Find the most recent peoplesgas_projects_YYYYMMDD.geojson file.

    Args:
        directory: Directory to search in

    Returns:
        Path to the most recent file, or None if not found
    """
    pattern = "peoplesgas_projects_*.geojson"
    files = list(directory.glob(pattern))

    if not files:
        return None

    # Sort by filename (YYYYMMDD format sorts chronologically)
    return sorted(files)[-1]


def main():
    """Upload the People's Gas GeoJSON file to S3."""
    utils_dir = Path(__file__).parent

    # Find the most recent dated GeoJSON file
    geojson_file = find_latest_geojson(utils_dir)

    if not geojson_file:
        print("❌ Error: No GeoJSON files found matching pattern 'peoplesgas_projects_*.geojson'")
        print(f"   Searched in: {utils_dir}")
        print("   Run 'just fetch-data' first to download the data")
        return 1

    print(f"📁 Found file: {geojson_file.name}")

    # Extract date from filename for S3 key
    filename = geojson_file.name  # e.g., peoplesgas_projects_20241104.geojson
    s3_key = f"gis/pgl/{filename}"

    # Upload to S3
    success = upload_to_s3(
        local_file=geojson_file,
        bucket="data.sb",
        s3_key=s3_key,
    )

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
