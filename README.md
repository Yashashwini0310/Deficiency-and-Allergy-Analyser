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

# Setup Instructions: (Cloud9 is used for this project)

# 1. Clone the repository:

git clone https://github.com/Yashashwini0310/cpp_project.git
cd allergy-analyzer

# 2. Create a virtual environment and install the dependencies:

python -m venv env
source env/bin/activate (linux based project)
pip install -r requirements.txt

# 3. setup AWS credentials using boto3.

# 4. Run the application locally first:

python manage.py migrate
python manage.py runserver 8080

# 5. Lastly, Deploy to Elastic Beantalk:

(deactivate the virtual environment and then perform below steps)

a. Helps in initializing the eb from terminal, you can provide any name of your choice, as this creates the function on AWS
eb init -p python-<version> <function_name> 
<for example: eb init -p python-3.9 AllergyAnalyzer>

b Helps in deploying the environment created
eb deploy or use eb deploy AllergyAnalyzer-env

# How to use:
1. Register/login the application
2. Enter Symtoms and get your report on possible results (deficiencies/allergy)
3. Subscribe to SNS alerts for notifications.
4. Accept the request on your mail. 
5. You will be notified everytime your symptoms are entered
6. you can also view SQS queue in the application.

# Known Issues and future Enhancements:
--Expand medical history database for better recommendations.
--Enhance UI for more user experience
--Add more AWS security measures.
--Enhance the analyzer by adding robust API for more accurate results.
