import base64
import json
import logging
import os
import uuid

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

BUCKET_NAME = "<BUCKET-NAME>"
s3 = boto3.client("s3")

API_KEY = os.getenv("API_KEY")


def lambda_handler(event, context):
    api_key = event.get("headers").get("x-api-key")

    if not api_key or api_key != API_KEY:
        return {"statusCode": 401, "body": json.dumps("Unauthorized")}
    method = event.get("httpMethod")
    if method != "POST":
        return {"statusCode": 401, "body": json.dumps("Method Not Allowed")}
    image_base64 = event.get("body")
    image_data = base64.b64decode(image_base64)
    file_id = str(uuid.uuid4())

    s3.put_object(Bucket=BUCKET_NAME, Key=f"{file_id}", Body=image_data)
    logger.info(f"create {file_id} into {BUCKET_NAME}")
    return {"statusCode": 201, "body": json.dumps(file_id)}
