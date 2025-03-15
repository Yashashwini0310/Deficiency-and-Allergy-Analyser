from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    symptoms = models.TextField(blank=True, null=True)  # Store symptoms
    severity_level = models.IntegerField(blank=True, null=True) # Store severity
    medical_history = models.TextField(blank=True, null=True)  # Store medical history
    report_url = models.CharField(max_length=255, blank=True, null=True) #for s3 url
    def __str__(self):
        return self.user.username

class Allergy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Deficiency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name