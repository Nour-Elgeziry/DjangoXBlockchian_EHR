from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerPatientPage/', views.registerPatientPage, name='registerPatientPage'),
    path('registerInsurance/', views.registerInsurancePage, name='registerInsurancePage'),
    path('registerMedicationPage/', views.registerMedicationPage, name='registerMedicationPage'),
    path('registerAlergiesPage/', views.registerAlergiesPage, name='registerAlergiesPage'),
]