import boto3
""" SNS handler to get and send messages to alert the user """
AWS_REGION = "us-east-1"
SNS_TOPIC_NAME = "SymptomAlertsTopic"
sns_client = boto3.client("sns", region_name=AWS_REGION) #create sns client
def get_sns_topic_arn():
    """Retrieve SNS topic ARN."""
    response = sns_client.list_topics() #list all sns topics
    for topic in response.get("Topics", []): #iterate through the list of topics
        if SNS_TOPIC_NAME in topic["TopicArn"]: #checks if the topic name is in the arn
            return topic["TopicArn"] #returns if found
    return None #returns none if not found
def send_sns_alert(message):
    """Publish a message to SNS."""
    topic_arn = get_sns_topic_arn() #gets the topicarn
    if not topic_arn: #checks if arn was found
        print("SNS Topic not found!") #prints error if not found
        return
    response = sns_client.publish( #publishes the message to the SNS topic
        TopicArn=topic_arn,
        Message=message
    )
    print(f"Sent SNS Alert: {message}") #prints message saying the allert was sent
if __name__ == "__main__":
    send_sns_alert("Alert: Symptom detected!")
