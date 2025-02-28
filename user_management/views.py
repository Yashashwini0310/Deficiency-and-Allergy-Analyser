from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, AllergyForm, DeficiencyForm
from .symptom_analysis.analyzer import analyze_symptoms
from .models import UserProfile, Allergy, Deficiency
from django.http import HttpResponse
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
import json

@csrf_exempt
def api_user_login(request):  # 🔹 Renamed function
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
    
@method_decorator(csrf_exempt, name='dispatch')
class SymptomSubmissionAPIView(APIView):
    authentication_classes = [TokenAuthentication]  # 🔹 Add this line
    permission_classes = [IsAuthenticated]  # Requires authentication

    def post(self, request):
        symptoms = request.data.get("symptoms", [])
        medical_history = request.data.get("medical_history", [])
        if not symptoms:
            return Response({"error": "Symptoms are required"}, status=status.HTTP_400_BAD_REQUEST)
        # Call analyze_symptoms() to get conditions, severity, and recommendations
        result = analyze_symptoms(symptoms, medical_history)
        # Example logic: Map symptoms to possible conditions
        # possible_conditions = []
        # if "fever" in symptoms:
        #     possible_conditions.append("Flu")
        # if "headache" in symptoms:
        #     possible_conditions.append("Migraine")
        # if "fatigue" in symptoms:
        #     possible_conditions.append("Anemia")
        # if "chest pain" in symptoms:
        #     possible_conditions.append("Heart Disease")
        # if not possible_conditions:
        #     possible_conditions.append("Unknown Condition")

        # return Response({"possible_conditions": possible_conditions}, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_200_OK)

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
    return render(request, 'user_management/login.html', {'form': form})

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Dashboard View (Symptom Analysis with Severity and medical history)
@login_required
def dashboard(request):
    result = None
    high_severity = False
    recommendation = None
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '').split(',')
        medical_history = request.POST.get('medical_history', '').split(',')
        print(f"Received symptoms: {symptoms}") #debugging
        print(f"Received medical history: {medical_history}") #debugging
        # process the symptoms and medical history
        analysis_result = analyze_symptoms(symptoms, medical_history)
        result = analysis_result.get('conditions')
        high_severity = 'Severe' in analysis_result.get('severity','')
        recommendation = analysis_result.get('recommendation')
        print(f"analysis_results: {result}")
        # # Set the high severity flag for display
        # if highest_severity in ["High", "Severe"]:
        #     high_severity = True

    return render(request, 'user_management/dashboard.html', {
        'result': result,
        'high_severity': high_severity,
        'recommendation': recommendation, # Ensure user context is passed
    })
    #     if symptoms:
    #         result = analyze_symptoms(symptoms, medical_history) 
    #         print(f"Analysis result: {result}")#passes the list 
    #         high_severity = any(item['severity'] == 'high' for item in result)
    #         #save symptoms and medical history to user profile
    #         profile, _ = UserProfile.objects.get_or_create(user=request.user)
    #         profile.symptoms = symptoms
    #         profile.medical_history = medical_history
    #         profile.save()
    # return render(request, 'user_management/dashboard.html', {'result': result, 'medical_history': medical_history, 'high_severity': high_severity})

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