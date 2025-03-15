"""This setup file creates SQS and SNS """
import boto3
# AWS Configuration
AWS_REGION = "us-east-1"  
SQS_QUEUE_NAME = "SymptomAlertsQueue"
SNS_TOPIC_NAME = "SymptomAlertsTopic"
# Initialize AWS clients
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
sns_client = boto3.client("sns", region_name=AWS_REGION)
#
def create_sqs_queue():
    """Create an SQS queue and return its URL & ARN."""
    response = sqs_client.create_queue(
        QueueName=SQS_QUEUE_NAME,
        Attributes={"VisibilityTimeout": "30"}  # 30 sec message visibility
    )
    queue_url = response["QueueUrl"]
    
    # Get Queue ARN
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=["QueueArn"]
    )
    queue_arn = response["Attributes"]["QueueArn"]

    print(f"SQS Queue Created: {queue_url}")
    return queue_url, queue_arn
#
def create_sns_topic():
    """Create an SNS topic and return its ARN."""
    response = sns_client.create_topic(Name=SNS_TOPIC_NAME)
    topic_arn = response["TopicArn"]
    print(f"SNS Topic Created: {topic_arn}")
    return topic_arn
#
def subscribe_sqs_to_sns(topic_arn, queue_arn):
    """Subscribe the SQS queue to the SNS topic."""
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="sqs",
        Endpoint=queue_arn
    )
    print(f"Subscribed SQS to SNS: {response['SubscriptionArn']}")
#
if __name__ == "__main__":
    queue_url, queue_arn = create_sqs_queue()
    topic_arn = create_sns_topic()
    subscribe_sqs_to_sns(topic_arn, queue_arn)
