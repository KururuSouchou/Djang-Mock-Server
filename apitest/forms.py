from django import forms
from .models import MyApi, MyApp

class AppForm(forms.ModelForm):
    class Meta:
        model = MyApp
        exclude = ['owner']

class ApiForm(forms.ModelForm):
    class Meta:
        model = MyApi
        exclude = ['app_name', 'owner']

class RegForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

