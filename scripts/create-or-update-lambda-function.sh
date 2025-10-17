#!/usr/bin/env bash
if aws lambda get-function --function-name $TARGET_LAMBDA_FUNCTION 2>&1 | grep -q 'ResourceNotFoundException'
then
  echo "Lambda function does not exist, creating..."
  aws lambda create-function \
    --function-name $TARGET_LAMBDA_FUNCTION \
    --runtime python3.12 \
    --timeout 30 \
    --handler $TARGET_LAMBDA_FUNCTION_HANDLER \
    --code "S3Bucket=$TARGET_S3_BUCKET,S3Key=$TARGET_S3_KEY" \
    --role "$TARGET_LAMBDA_ROLE" \
    --environment Variables="{SJ_CONTRACTS_PATH=/tmp,SJ_LOG_PATH=/tmp/shioaji.log}"
else
  echo "Lambda function already exists, updating"
  aws lambda update-function-code --function-name ${TARGET_LAMBDA_FUNCTION} --s3-bucket ${TARGET_S3_BUCKET} --s3-key ${TARGET_S3_KEY}
  aws lambda update-function-configuration --function-name ${TARGET_LAMBDA_FUNCTION} --runtime python3.12
fi