from django.http import HttpResponse
import json
import logging
import os
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .symptom_analysis.analyzer import analyze_symptoms
from .models import UserProfile, Allergy, Deficiency
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserProfileSerializer, AllergySerializer, DeficiencySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.authtoken.models import Token 
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from aws_services.sqs_handler import receive_sqs_messages, send_message_to_sqs
from aws_services.sns_handler import send_sns_alert
from aws_services.s3_handler import upload_to_s3
from .utils import generate_presigned_url
from aws_services.dynamodb_handler import store_analysis, retrieve_analysis_history
from .forms import UserRegistrationForm, UserLoginForm, AllergyForm, DeficiencyForm



# AWS Configuration
AWS_REGION = "us-east-1"
AWS_LAMBDA_FUNCTION_NAME = "SymptomAnalysisLambda"
lambda_client = boto3.client("lambda", region_name=AWS_REGION)

# CloudWatch Logger
logger = logging.getLogger("django")

# unified Lambda Invocation Function
def invoke_lambda(symptoms, medical_history):
    payload = {
        "body": json.dumps({
            "symptoms": symptoms,
            "medical_history": medical_history
        })
    }

    try:
        response = lambda_client.invoke(
            FunctionName=AWS_LAMBDA_FUNCTION_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))
        result = json.loads(response_payload.get("body", "{}"))

        severity = result.get("severity", "Unknown")  # ✅ Correct extraction of severity
        return {
            "conditions": result.get("conditions", []),
            "severity": severity,
            "recommendation": result.get("recommendation", [])
        }

    except Exception as e:
        logger.error(f"Lambda invocation error: {e}")
        return {"error": "Failed to process request"}

# ✅ User Login API
@csrf_exempt
def api_user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({"token": token.key}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# ✅ Dashboard View (Calls Lambda)
@login_required
def dashboard(request):

    #Handles the user dashboard, including symptom analysis and report generation.

    logger.info(f"Dashboard accessed by user: {request.user}")
    result = None
    recommendation = None
    severity_level = None
    symptoms_str = ""  # Initializes symptoms_str here
    medical_history_str = "" # Initializes medical_history_str here
    messages = receive_sqs_messages()
    conditions = []
    analysis_history = []
    if request.method == "POST":
        # Retrieve user input from the form
        symptoms_str = request.POST.get("symptoms", "").strip()
        medical_history_str = request.POST.get("medical_history", "").strip()

        # Ensure valid inputs to process into lists
        symptoms = [s.strip() for s in symptoms_str.split(",") if s.strip()]
        medical_history = [m.strip() for m in medical_history_str.split(",") if m.strip()]

        logger.info(f"Received Symptoms: {symptoms}, Medical History: {medical_history}")

        if symptoms:
            try: # **Update UserProfile with raw input
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.symptoms = symptoms_str # Save raw     string for display at the top
                user_profile.medical_history = medical_history_str     # Save raw string
                user_profile.save()
            except UserProfile.DoesNotExist:
                logger.error(f"UserProfile does not exist for user: {request.user.username}")
            
            # Send SNS Alert to notify about symptom report
            alert_message = f"User {request.user.username} reported symptoms: {symptoms}"
            send_sns_alert(alert_message)
            
             # Invoke AWS Lambda Function for symptom analysis
            result = invoke_lambda(symptoms, medical_history)
            logger.info(f"Raw Lambda Result: {result}")
            
             # Extract analysis results from Lambda response
            conditions = result.get("conditions", [])
            severity_level = result.get("severity")
            recommendation = result.get("recommendation")
            #debug
            print(f"result: {result}; severity_level: {severity_level}; conditions: {conditions}; recommendations: {recommendation}")
            logger.info(f"Lambda Result: {result}")  # Corrected logging
            
            # Send Analysis Result to SQS for further processing
            sqs_message = {
                "user": request.user.username,
                "symptoms": symptoms,
                "result": result
            }
            send_message_to_sqs(sqs_message)
            print(messages)
            # Save results to a JSON file
            report_filename = f"{request.user.username}_report.pdf"
            report_path = os.path.join(settings.MEDIA_ROOT, report_filename)
            
            try:
                c = canvas.Canvas(report_path, pagesize=letter)
                c.drawString(1 * inch, 10 * inch, f"Report for {request.user.username}")
                y = 9 * inch
                for key, value in result.items():
                    c.drawString(1 * inch, y, f"{key}: {value}")
                    y -= 0.5 * inch
                c.save()
                logger.info(f"PDF report created: {report_path}")

            except Exception as e:
                logger.error(f"Error creating PDF report: {e}")
                return render(request, "user_management/dashboard.html", {"error": "Error creating PDF report."})

            #uploads the report file to s3 and generate preseigned URL
            upload_to_s3(report_path, report_filename)
            s3_url = generate_presigned_url(settings.AWS_STORAGE_BUCKET_NAME, report_filename)
            # logger.info(f"Pre-signed URL from generate_presigned_url: {s3_url}")
            
            # Store analysis in DynamoDB
            store_analysis(request.user.username, symptoms_str, 
            medical_history_str, result, report_filename)
            
            # Fetch previous analysis history
            analysis_history = retrieve_analysis_history(request.user.username)
            
            #saves the s3 URL to the user profile
            if s3_url:
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    # logger.info(f"Saving report URL to profile: {s3_url}") #debugging
                    user_profile.report_url = s3_url
                    user_profile.save()
                    # logger.info(f"Report URL saved to profile.") #debugging to see if the file saved
                except UserProfile.DoesNotExist:
                    logger.error(f"UserProfile does not exist for user: {request.user.username}")
    # Log the report URL for debugging
    report_url_log = request.user.userprofile.report_url 
    if hasattr(request.user, 'userprofile') and hasattr(request.user.userprofile, 'report_url') 
    else 'UserProfile or report_url missing'
    logger.debug(f"Rendering dashboard with report_url: {request.user.userprofile.report_url if hasattr(request.user, 'userprofile') else 'No UserProfile'}")

# Render the dashboard template   
    return render(request, "user_management/dashboard.html", {
        "messages": messages, #I want the sqs message in my dashboard. 
        "symptoms": symptoms_str,
        "conditions":conditions,
        "result": result,
        "severity_level": severity_level,
        "recommendation": recommendation,
        "disclaimer": "This is just a predicted analysis. Kindly consult your doctor for more info. The results can be inaccurate.",
        "analysis_history": analysis_history
})

# API View for Symptom Submission (Calls Lambda)
@method_decorator(csrf_exempt, name="dispatch")
class SymptomSubmissionAPIView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        symptoms = request.data.get("symptoms", [])
        medical_history = request.data.get("medical_history", [])

        if not symptoms:
            logger.warning("API Request Missing Symptoms")
            return Response({"error": "Symptoms are required"}, status=400)

        # Invoke Lambda
        result = invoke_lambda(symptoms, medical_history)
        logger.info(f"User: {request.user.username} | Symptoms: {symptoms} | Medical History: {medical_history} | Lambda Result: {result}")

        return Response(result, status=200)

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_management/register.html', {'form': form})

# User Login View
@login_required
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# CRUD for Allergy
@login_required
def allergy_list(request):
    allergies = Allergy.objects.all()
    return render(request, 'user_management/allergy_list.html', {'allergies': allergies})

@login_required
def allergy_create(request):
    if request.method == 'POST':
        form = AllergyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allergy_list')
    else:
        form = AllergyForm()
    return render(request, 'user_management/allergy_form.html', {'form': form})

@login_required
def allergy_update(request, pk):
    allergy = get_object_or_404(Allergy, pk=pk)
    if request.method == 'POST':
        form = AllergyForm(request.POST, instance=allergy)
        if form.is_valid():
            form.save()
            return redirect('allergy_list')
    else:
        form = AllergyForm(instance=allergy)
    return render(request, 'user_management/allergy_form.html', {'form': form})

@login_required
def allergy_delete(request, pk):
    allergy = get_object_or_404(Allergy, pk=pk)
    if request.method == 'POST':
        allergy.delete()
        return redirect('allergy_list')
    return render(request, 'user_management/allergy_confirm_delete.html', {'allergy': allergy})

# CRUD for Deficiency
@login_required
def deficiency_list(request):
    deficiencies = Deficiency.objects.all()
    return render(request, 'user_management/deficiency_list.html', {'deficiencies': deficiencies})

@login_required
def deficiency_create(request):
    if request.method == 'POST':
        form = DeficiencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deficiency_list')
    else:
        form = DeficiencyForm()
    return render(request, 'user_management/deficiency_form.html', {'form': form})

@login_required
def deficiency_update(request, pk):
    deficiency = get_object_or_404(Deficiency, pk=pk)
    if request.method == 'POST':
        form = DeficiencyForm(request.POST, instance=deficiency)
        if form.is_valid():
            form.save()
            return redirect('deficiency_list')
    else:
        form = DeficiencyForm(instance=deficiency)
    return render(request, 'user_management/deficiency_form.html', {'form': form})

@login_required
def deficiency_delete(request, pk):
    deficiency = get_object_or_404(Deficiency, pk=pk)
    if request.method == 'POST':
        deficiency.delete()
        return redirect('deficiency_list')
    return render(request, 'user_management/deficiency_confirm_delete.html', {'deficiency': deficiency})

@method_decorator(csrf_exempt, name='dispatch')
# API to fetch and update user profile (including symptoms & medical history)
class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request):
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        symptoms = request.data.get('symptoms', '')
        medical_history = request.data.get('medical_history', '')

        # Analyze symptoms and determine severity
        result = analyze_symptoms(symptoms.split(','), medical_history)

        user_profile.symptoms = symptoms
        user_profile.medical_history = medical_history
        user_profile.save()

        return Response({"message": "Symptoms updated successfully", "analysis": result})


# API to fetch all allergies
class AllergyListAPIView(generics.ListCreateAPIView):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# API to fetch all deficiencies
class DeficiencyListAPIView(generics.ListCreateAPIView):
    queryset = Deficiency.objects.all()
    serializer_class = DeficiencySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ProtectedAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"}, status=200)
#test endpoint for symptom submission

#Cloudwatch loggings below
#ogging to track API requests and errors

