from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('registerPatient/', views.registerPatient, name='registerPatient'),
    path('registerInsurance/', views.registerInsurance, name='registerInsurance'),
    path('registerMedication/', views.registerMedication, name='registerMedication'),
    path('registerAlergies/', views.registerAlergies, name='registerAlergies'),
]