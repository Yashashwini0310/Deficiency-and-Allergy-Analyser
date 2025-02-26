from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Allergy, Deficiency

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    symptoms = forms.CharField(widget=forms.Textarea(), required=False)
    medical_history = forms.CharField(widget=forms.Textarea(), required=False)  # New field

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # UserProfile is created or updated with the symptoms later in views.py
            UserProfile.objects.create(
                user=user,
                symptoms=self.cleaned_data['symptoms'],
                medical_history=self.cleaned_data['medical_history']  # Save medical history
            )
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['symptoms', 'medical_history']

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['name', 'description']

class DeficiencyForm(forms.ModelForm):
    class Meta:
        model = Deficiency
        fields = ['name', 'description']