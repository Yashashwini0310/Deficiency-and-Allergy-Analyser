import boto3
import json
import logging

logger = logging.getLogger(__name__)
AWS_REGION = "us-east-1"
SQS_QUEUE_NAME = "SymptomAlertsQueue"

sqs_client = boto3.client("sqs", region_name=AWS_REGION)

def get_sqs_queue_url():
    """Fetch the SQS queue URL with error handling."""
    try:
        response = sqs_client.get_queue_url(QueueName=SQS_QUEUE_NAME)
        return response["QueueUrl"]
    except Exception as e:
        logger.error(f"Error fetching SQS queue URL: {e}") # Log the error
        return None # Or raise an exception again, or return a default URL if appropriate for your case. Returning None is often a good choice.

def send_message_to_sqs(message_body):
    """Sends a message to the SQS queue, handling queue URL errors."""
    queue_url = get_sqs_queue_url()
    if not queue_url: # Check if queue_url is None (error occurred in get_sqs_queue_url)
        logger.error("Cannot send message to SQS because queue URL is None.")
        return False # Indicate failure to send message
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body)
        )
        print(f"Message sent to SQS: {response['MessageId']}")
        return True # Indicate successful message sending
    except Exception as e:
        logger.error(f"Error sending message to SQS: {e}")
        return False # Indicate failure to send message

def receive_sqs_messages():
    """Retrieve messages from SQS with error handling."""
    messages_list = [] # Initialize list to return even if errors occur
    try:
        queue_url = get_sqs_queue_url() # Get queue URL - Ensure this function handles errors as well
        if not queue_url: # Check if get_sqs_queue_url returned None (error)
            logger.error("SQS queue URL is None, cannot proceed to receive messages.")
            return ["Error: Could not retrieve system messages. Queue URL not found."] # Return user-friendly error

        response = sqs_client.receive_message( # Try to receive messages
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        messages_data = response.get("Messages", []) # Safe access in case 'Messages' key is missing

        for msg_data in messages_data:
            try: # Inner try-except for processing each message to prevent one bad message from stopping all
                message_body = msg_data['Body'] # Extract message body
                messages_list.append(message_body) # Add to list
                print(f"Received and Processed SQS Message: {message_body}") # Log processing

            # Delete the message after successful processing
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg_data["ReceiptHandle"]
                )
                print(f"Deleted SQS Message with ReceiptHandle: {msg_data['ReceiptHandle']}") # Log deletion
            except Exception as processing_error:
                logger.error(f"Error processing SQS message: {processing_error}, ReceiptHandle: {msg_data.get('ReceiptHandle', 'N/A')}", exc_info=True) # Log error for individual message processing

    except Exception as e:
        logger.error(f"Error retrieving or processing SQS messages: {e}") # Log detailed error
        messages_list = ["Error retrieving system messages. Please check logs."] # User-friendly error message to display on dashboard
        # Or you could return an empty list `return []` if you don't want to display an error message on dashboard, but just want to handle error silently.

    return messages_list # Return the list of messages (could be empty or contain error message in case of failure)
    
if __name__ == "__main__":
    receive_sqs_messages()
