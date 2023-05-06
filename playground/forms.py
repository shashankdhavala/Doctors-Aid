from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Doctor,Patient,Report

# Create your models here.
class doctor_login(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
    #    widgets={'password':forms.PasswordInput()}
        fields=('username','password')


class signup_form_doc (forms.ModelForm):
    class Meta:
        model=Doctor
        widgets={'password':forms.PasswordInput()}
        fields=('email_id','first_name','last_name','password')

class signup_form_patient(forms.ModelForm):

    class Meta:
        model=Patient
        fields={'first_name','last_name','Age','Gender'}

class add_report_form(forms.ModelForm):
    img=forms.ImageField()
    class Meta:
        model=Report
        fields={'disease_name','img'}
