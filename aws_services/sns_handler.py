import boto3

AWS_REGION = "us-east-1"
SNS_TOPIC_NAME = "SymptomAlertsTopic"

sns_client = boto3.client("sns", region_name=AWS_REGION)

def get_sns_topic_arn():
    """Retrieve SNS topic ARN."""
    response = sns_client.list_topics()
    for topic in response.get("Topics", []):
        if SNS_TOPIC_NAME in topic["TopicArn"]:
            return topic["TopicArn"]
    return None

def send_sns_alert(message):
    """Publish a message to SNS."""
    topic_arn = get_sns_topic_arn()
    if not topic_arn:
        print("SNS Topic not found!")
        return

    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    print(f"Sent SNS Alert: {message}")

if __name__ == "__main__":
    send_sns_alert("Alert: Symptom detected!")
