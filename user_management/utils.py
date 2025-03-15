import logging
from django.conf import settings
import boto3
#this is to make sure that the authenticated user gets the report, due to less IAM credentials
logger = logging.getLogger(__name__)

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a pre-signed URL to share an S3 object."""
    s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        logger.info(f"Generated pre-signed URL for {object_name}")
    except Exception as e:
        logger.error(f"Error generating pre-signed URL: {e}")
        return None

    return response