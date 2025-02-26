from django.urls import path
from .views import user_register, user_login, user_logout, dashboard, UserProfileAPIView, AllergyListAPIView, DeficiencyListAPIView, SymptomSubmissionAPIView
from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Allergy URLs
    path('allergies/', views.allergy_list, name='allergy_list'),
    path('allergies/create/', views.allergy_create, name='allergy_create'),
    path('allergies/<int:pk>/update/', views.allergy_update, name='allergy_update'),
    path('allergies/<int:pk>/delete/', views.allergy_delete, name='allergy_delete'),
    
    # Deficiency URLs
    path('deficiencies/', views.deficiency_list, name='deficiency_list'),
    path('deficiencies/create/', views.deficiency_create, name='deficiency_create'),
    path('deficiencies/<int:pk>/update/', views.deficiency_update, name='deficiency_update'),
    path('deficiencies/<int:pk>/delete/', views.deficiency_delete, name='deficiency_delete'),
    
    #API URLs
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile-api'),
    path('allergies/', AllergyListAPIView.as_view(), name='allergy-list-api'),
    path('deficiencies/', DeficiencyListAPIView.as_view(), name='deficiency-list-api'),
    path('symptoms/', SymptomSubmissionAPIView.as_view(), name='symptoms-submit-api'),
]
