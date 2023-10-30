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

    if method != "DELETE":
        return {"statusCode": 401, "body": json.dumps("Method Not Allowed")}

    object_key = event.get("path").rsplit("/", 1)[-1]
    s3.delete_object(Bucket=BUCKET_NAME, Key=object_key)

    logger.info(f"Delete {object_key} from {BUCKET_NAME}")
    return {"statusCode": 204, "body": json.dumps("Object deleted successfully.")}
