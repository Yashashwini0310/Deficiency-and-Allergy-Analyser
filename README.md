# cpp_project
This is a web-based application called "Allergy and Deficiency Analyzer".

# Description:
Motivation for this project - There are several disease accross the world, and many cannot afford large fees for their diagnosed medical issues.
This projects aims to build a gap between initial symptoms and professional diagnosis where patients/users can know beforehand what are their symptoms and why is it occuring, what are the recommendations.
This cloud-based application helps users to analyze their symptoms and provides possible conditions based upon their inputs.
This project is integrated using 6 AWS services, they are AWS Lambda, SNS, SQS, DynamoDB, S3 and Cloudwatch.
The Dashboard also displays the SQS queue message on the application to display users/developers how the SQS handles the message queue.
The UI of the Dashboard displays Home, Allergies, Deficiencies, Logout.
Home button provides dashboard for users to analyse their symptoms. 
Allergies and Deficiencies on the dashboard provides users to add, delete, update, read their added allergies and deficiencies on their profile.

# Features of this Project:
Authenticates user and manages the profile.
Symtom-based analysis with recommendations
Cloud based database and file storage using AWS.
Notification alerts via AWS SNS.
Secure message processing using AWS SQS.
CI/CD pipeline with GitHub actions.
Static Code Analysis using pylint.
Custom Python library for Symptom analysis.

**#technologies used are:**
For Backend:
    --Django, python
For Cloud Services:
    --AWS Cloudwatch, S3, DynamoDB, SNS, SQS, Lambda
For CI/CD:
    --GitHub Actions
For Static Code Analysis:
    --Pylint
For Frontend:
    --HTML, CSS
Custom Library:
    I have created a custom library to handle the data for analysis when a user provides the symptoms on the dashboard.
    --https://pypi.org/project/symptom-analysis/1.0.2/

# This Project is Deployed in AWS using Elastic Beanstalk:
    http://allergyanalyzersystem-env.eba-eyus5yb4.us-east-1.elasticbeanstalk.com/

# About AWS services used in this project and reason for them:
# 1. AWS Elastic Beanstalk:
purpose:
Elastic beanstalk simplifies the scaling, management and deployment of web applications.
Why was it used: 
Easy deployment
Built-in Monitoring facility.

# 2. AWS Simple Notification Service (SNS):

purpose:
SNS is a messaging service providing facility to alert users via email/SMS.

why was this used:
It provides easy subscription.
Messages are reliable.
Real-time Alerts to users.

# 3. AWS Simple Queue Service (SQS)

purpose:
SQS is a queuing system used to handle the processing of messages.

why was this used:
Ensures asynchronous processing like when users enter symptoms the analysis requests are queued.
Preventing overloading of messages.
Reliable delivery of message processing.

# 4. AWS DynamoDB

purpose:
DynamoDB is a NoSQL database for storing user data and their symptom history.

why was this used:
Scalability - Scales automatically based on the loads.
high availability as data is being replicated across many AWS regions.
No need for the database maangement

# 5. S3 (Simple Storage Service)

purpose:
S3 provides storage facilities in AWS for files generated from the analysis on the dashboard.

# Setup Instructions: (Cloud9 is used for this project)

# 1. Clone the repository:

git clone https://github.com/Yashashwini0310/cpp_project.git
cd allergy-analyzer

# 2. Create a virtual environment and install the dependencies:

python -m venv env
source env/bin/activate (linux based project)
pip install -r requirements.txt

# 3. If using Learners lab, check if these AWS are accessible and setup AWS credentials using boto3 accordingly

# 4. Run the application locally first:

python manage.py migrate
python manage.py runserver 8080

# 5. Lastly, Deploy to Elastic Beantalk:

(deactivate the virtual environment and then perform below steps)
a. install awsebcli : pip install awsebcli

b. Helps in initializing the eb from terminal, you can provide any name of your choice, as this creates the function on AWS
eb init -p python-<version> <function_name> 
<for example: eb init -p python-3.9 AllergyAnalyzer>

c. Helps in deploying the environment created
eb deploy or use eb deploy AllergyAnalyzer-env

d. you can open your deployed AWS domain of your project using below command
eb open

# For testing
Run tests Locally:
python3 manage.py test

Run Pylint for Static Code Analysis locally
if your root folder is Allergy_Analyzer:
pylint Allergy_Analyzer
if you want to run for each folder use:
pylint user_management/

# How to use:
1. Register/login the application
2. Enter Symtoms (example: Fever, headache, fatigue, chest pain, cough) 
   Enter your Medical history if available (eg. diabetes, Heart Disease, Hypertension, Asthma) 
   Get your report on possible results (deficiencies/allergy)
3. Subscribe to SNS alerts for notifications.
4. Accept the request on your mail. 
5. You will be notified everytime your symptoms are entered
6. you can also view SQS queue in the application.

# Please Note 
This project has manual datasets provided for the analysis. Hence the medical history is limited, you can provide above example medical history for testing.

# Known Issues and future Enhancements:
--Expand medical history database for better recommendations.
--Enhance UI for more user experience
--Add more AWS security measures.
--Enhance the analyzer by adding robust API for more accurate results.


# Author : Yashashwini
# linkedIn : https://www.linkedin.com/in/yashashwini-s-485283190/

# Home Page, Login Page, Subscribe, allergy and deficieny ribbon.
![image](https://github.com/user-attachments/assets/c04a47a3-8616-42cf-a768-b832b78c3b63)

![image](https://github.com/user-attachments/assets/8e4254fd-6888-4db4-9684-55c2b780d248)

# Dashboard before and after entering symptoms
![image](https://github.com/user-attachments/assets/0a23fd74-6e99-4bff-a09a-13d8ff2ebc17)
![image](https://github.com/user-attachments/assets/8a384812-4b0d-4493-8b0c-1e43e72e22e9)

# Subscribe to news page
![image](https://github.com/user-attachments/assets/308df69b-e7c6-4d5f-8e1c-440c09b8843e)

# Deficiency and Allergy Page
![image](https://github.com/user-attachments/assets/f84e303d-7012-402e-aebe-dee476726bf8)
![image](https://github.com/user-attachments/assets/831da49b-9b2a-42b1-9161-a5d397c4dc6b)





