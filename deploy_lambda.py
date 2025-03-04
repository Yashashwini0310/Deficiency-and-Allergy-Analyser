# import boto3
# import json

# lambda_client = boto3.client('lambda', region_name="us-east-1")

# function_name = "SymptomAnalysisLambda"
# runtime = "python3.8"
# handler = "lambda_function.lambda_handler"

# # Read the zip file
# with open("lambda_function.zip", "rb") as f:
#     zip_content = f.read()

# # Deploy Lambda using existing AWS Lab role
# response = lambda_client.create_function(
#     FunctionName=function_name,
#     Runtime=runtime,
#     Role="arn:aws:sts::091200948475:assumed-role/voclabs/user3805467=x23251263@student.ncirl.ie",  # Use assigned role
#     Handler=handler,
#     Code={"ZipFile": zip_content},
#     Timeout=30,
#     MemorySize=128
# )

# print(json.dumps(response, indent=4))
import boto3

LAMBDA_NAME = "SymptomAnalysisLambda"
ROLE_ARN = "arn:aws:iam::091200948475:role/LabRole"  # Your Learner Lab Role

lambda_client = boto3.client("lambda", region_name="us-east-1")

def deploy_lambda():
    # Read the ZIP file
    with open("lambda_function.zip", "rb") as f:
        zip_content = f.read()

    response = lambda_client.create_function(
        FunctionName=LAMBDA_NAME,
        Runtime="python3.9",
        Role=ROLE_ARN,
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": zip_content},  # Directly upload ZIP 
        Timeout=10,
        MemorySize=128,
    )
    
    print(f"Lambda {LAMBDA_NAME} created successfully!")
    print(response)

if __name__ == "__main__":
    deploy_lambda()
