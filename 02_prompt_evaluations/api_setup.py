import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def setup():
    load_dotenv()

    model_id = os.getenv("INFERENCE_PROFILE")
    if not model_id:
        raise ValueError("INFERENCE_PROFILE is required")

    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    return client, model_id
    