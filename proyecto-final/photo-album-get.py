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

    if method != "GET":
        return {"statusCode": 401, "body": json.dumps("Method Not Allowed")}

    object_key = event.get("path").rsplit("/", 1)[-1]
    logger.info(f"Retrieve {object_key} from {BUCKET_NAME}")

    response = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)

    file_content = response["Body"].read()

    file_path = "/tmp/output.png"

    with open(file_path, "wb") as f:
        f.write(file_content)

    with open(file_path, "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    os.remove(file_path)

    return {
        "statusCode": 200,
        "body": encoded_image,
        "isBase64Encoded": True,
        "headers": {
            "Content-Type": "image/png",
            "Content-Disposition": f'attachment; filename="{object_key}.png"',
        },
    }
