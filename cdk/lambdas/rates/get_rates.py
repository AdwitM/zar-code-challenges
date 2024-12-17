import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["MAIN_TABLE"])


def handler(event, context):
    try:
        response = table.query(
            KeyConditionExpression=Key("pk").eq("RATE") & Key("sk").begins_with("#"),
            ScanIndexForward=False,  # Get latest first
        )
        items = response.get("Items", [])

        rates = {}
        for item in items:
            pair = item["pair"]
            if pair not in rates:
                rates[pair] = item["rate"]

        return {"statusCode": 200, "body": json.dumps(rates)}

    except Exception as e:
        print(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error."}),
        }
