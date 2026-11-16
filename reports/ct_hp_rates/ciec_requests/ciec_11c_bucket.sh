#!/usr/bin/env bash
# Public S3 bucket for the CIEC-11(c) CAIRO files (Docket 26-05-10).
#
#   setup   create the bucket private (all public access blocks on) and its budget alert
#   open    allow anonymous read and list of the CIEC-11(c) prefix only
#   close   remove public access (the response to a budget alert)
#   status  print the bucket's access, encryption, versioning and tags
#
# Every command can be rerun; it reapplies the same settings. Deletion after the docket
# closes is tracked in Linear R2-190.
set -euo pipefail

BUCKET="switchbox-public-data"
REGION="us-west-2"
TAG_PROJECT="ct-hp-rates-ciec-11c"
BUDGET_NAME="switchbox-public-data bucket"
BUDGET_USD="20"
ALERT_EMAILS=("alex@switch.box" "lizzy@switch.box")
PATH_POLICY="$(dirname "$0")/ciec_11c_bucket_policy.json"

block_all() {
  aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
}

setup() {
  if aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
    echo ">> $BUCKET exists; reapplying settings"
  else
    echo ">> Creating $BUCKET in $REGION"
    aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" \
      --create-bucket-configuration LocationConstraint="$REGION" \
      --object-ownership BucketOwnerEnforced
  fi
  block_all
  aws s3api put-bucket-ownership-controls --bucket "$BUCKET" \
    --ownership-controls 'Rules=[{ObjectOwnership=BucketOwnerEnforced}]'
  aws s3api put-bucket-encryption --bucket "$BUCKET" --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"},"BucketKeyEnabled":false}]}'
  aws s3api put-bucket-tagging --bucket "$BUCKET" \
    --tagging "TagSet=[{Key=project,Value=$TAG_PROJECT},{Key=public,Value=true}]"

  local account
  account="$(aws sts get-caller-identity --query Account --output text)"
  if aws budgets describe-budget --account-id "$account" --budget-name "$BUDGET_NAME" >/dev/null 2>&1; then
    echo ">> Budget '$BUDGET_NAME' exists"
  else
    echo ">> Creating budget '$BUDGET_NAME' (\$$BUDGET_USD/month, alerts at 25% and 100% of actual)"
    local subscribers="" email
    for email in "${ALERT_EMAILS[@]}"; do
      subscribers+="{\"SubscriptionType\":\"EMAIL\",\"Address\":\"$email\"},"
    done
    subscribers="[${subscribers%,}]"
    aws budgets create-budget --account-id "$account" \
      --budget "{\"BudgetName\":\"$BUDGET_NAME\",\"BudgetLimit\":{\"Amount\":\"$BUDGET_USD\",\"Unit\":\"USD\"},\"TimeUnit\":\"MONTHLY\",\"BudgetType\":\"COST\",\"CostFilters\":{\"TagKeyValue\":[\"user:project\$$TAG_PROJECT\"]}}" \
      --notifications-with-subscribers "[
				{\"Notification\":{\"NotificationType\":\"ACTUAL\",\"ComparisonOperator\":\"GREATER_THAN\",\"Threshold\":25,\"ThresholdType\":\"PERCENTAGE\"},\"Subscribers\":$subscribers},
				{\"Notification\":{\"NotificationType\":\"ACTUAL\",\"ComparisonOperator\":\"GREATER_THAN\",\"Threshold\":100,\"ThresholdType\":\"PERCENTAGE\"},\"Subscribers\":$subscribers}
			]"
  fi
  echo ">> $BUCKET is set up and private"
}

open() {
  aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false
  aws s3api put-bucket-policy --bucket "$BUCKET" --policy "file://$PATH_POLICY"
  echo ">> $BUCKET: anonymous read and list of ct_hp_rates/pura_26-05-10/ciec-11c/ are on"
}

close() {
  aws s3api delete-bucket-policy --bucket "$BUCKET"
  block_all
  echo ">> $BUCKET is private again"
}

status() {
  echo "== public access block"
  aws s3api get-public-access-block --bucket "$BUCKET" --query PublicAccessBlockConfiguration --output json
  echo "== policy is public"
  aws s3api get-bucket-policy-status --bucket "$BUCKET" --query PolicyStatus.IsPublic --output text 2>/dev/null || echo "no policy"
  echo "== ownership / encryption / versioning"
  aws s3api get-bucket-ownership-controls --bucket "$BUCKET" --query 'OwnershipControls.Rules[0].ObjectOwnership' --output text
  aws s3api get-bucket-encryption --bucket "$BUCKET" \
    --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output text
  aws s3api get-bucket-versioning --bucket "$BUCKET" --query Status --output text
  echo "== tags"
  aws s3api get-bucket-tagging --bucket "$BUCKET" --output text
}

case "${1:-}" in
setup | open | close | status) "$1" ;;
*)
  echo "usage: $0 {setup|open|close|status}" >&2
  exit 1
  ;;
esac
