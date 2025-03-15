import logging
import boto3
"""s3_setup file is to create an s3 bucket in AWS programatically """
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level

# AWS Configuration
AWS_REGION = "us-east-1"
BUCKET_NAME = "allergy-analyzer-reports"

def create_s3_bucket():
    """Create an S3 bucket if it doesn't exist."""
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME)  # Removed LocationConstraint for us-east-1
        logger.info(f"S3 bucket '{BUCKET_NAME}' created successfully.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"S3 bucket '{BUCKET_NAME}' already exists.")
    except Exception as e:
        logger.error(f"Error creating S3 bucket: {e}")

if __name__ == "__main__":
    create_s3_bucket()