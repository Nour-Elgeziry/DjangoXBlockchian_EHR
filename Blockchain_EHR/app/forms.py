from django import forms

class LoginForm(forms.Form):
    address = forms.CharField(label ='Address', max_length=200)
    privateKey = forms.CharField(label ='Address', max_length=200)

class PatientForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    dob = forms.CharField(label='Dob', max_length=100)
    postCode = forms.CharField(label='Post Code', max_length=100)
    height = forms.CharField(label='Height', max_length=100)
    weight = forms.CharField(label='Weight', max_length=100)

class InsuranceForm(forms.Form):
    insuranceNumber = forms.CharField(label='Insurance Number', max_length=100)

class MedicationForm(forms.Form):
    medicine = forms.CharField(label='Medicine', max_length=100)

class AlergiesForm(forms.Form):
    alergy = forms.CharField(label='Alergy', max_length=100)
