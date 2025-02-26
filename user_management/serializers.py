from rest_framework import serializers
from .models import UserProfile, Allergy, Deficiency

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'symptoms', 'medical_history']

class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

class DeficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deficiency
        fields = '__all__'
