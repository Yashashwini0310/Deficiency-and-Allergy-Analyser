import logging
import boto3
"""dynamodb_setup file code below created dynamodb table programatically
helps in storing report files from the user dashboard"""
logger = logging.getLogger(__name__)

AWS_REGION = "us-east-1"
TABLE_NAME = "AllergyAnalysisHistory"

def create_dynamodb_table():
    """Create DynamoDB table for storing analysis history."""
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

    try:
        existing_tables = dynamodb.list_tables()["TableNames"]
        if TABLE_NAME in existing_tables:
            logger.info(f"Table '{TABLE_NAME}' already exists.")
            return
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "username", "KeyType": "HASH"},
                       {"AttributeName": "timestamp", "KeyType": "RANGE"}],
            AttributeDefinitions=[{"AttributeName": "username", "AttributeType": "S"},
                                  {"AttributeName": "timestamp", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )

        logger.info(f"Table '{TABLE_NAME}' creation in progress: {response}")
    except Exception as e:
        logger.error(f"Error creating table: {e}")

if __name__ == "__main__":
    create_dynamodb_table()
