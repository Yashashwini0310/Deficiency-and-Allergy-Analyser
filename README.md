# cpp_project
This is a web-based application called "Allergy and Deficiency Analyzer".

#Description:
This cloud-based application helps users to analyze their symptoms and provides possible conditions based upon their inputs.
This project is integrated using 6 AWS services. 
They are AWS Lambda, SNS, SQS, DynamoDB, S3 and Cloudwatch.
The Dashboard also displays the SQS queue message on the application.

#Features of this Project:
Authenticates user and manages the profile.
Symtom-based analysis with recommendations
Cloud based database and file storage using AWS.
Notification alerts via AWS SNS.
Secure message processing using AWS SQS.
CI/CD pipeline with GitHub actions.
Static Code Analysis using pylint.

#technologies used are:
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

#Setup Instructions: (Cloud9 is used for this project)

1. Clone the repository:

git clone https://github.com/Yashashwini0310/cpp_project.git
cd allergy-analyzer

2. Create a virtual environment and install the dependencies:

python -m venv env
source env/bin/activate (linux based project)
pip install -r requirements.txt

3. setup AWS credentials using boto3:

4. Run the application locally first:

python manage.py migrate
python manage.py runserver

5. Lastly, Deploy to Elastic Beantalk:

(deactivate the virtual environment and then perform below steps)
eb init -p python-3.9 AllergyAnalyzer
eb deploy

#How to use:
1. Register/login the application
2. Enter Symtoms and get your report on possible results (deficiencies/allergy)
3. Subscribe to SNS alerts for notifications.
4. Accept the request on your mail. 
5. You will be notified everytime your symptoms are entered
6. you can also view SQS queue in the application.

#Known Issues and future Enhancements:
--Expand medical history database for better recommendations.
--Enhance UI for more user experience
--Add more AWS security measures.
--Enhance the analyzer by adding robust API for more accurate results.