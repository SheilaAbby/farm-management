import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.')
    role = forms.ChoiceField(choices=[('farmer', 'Farmer'), ('field_agent', 'Field Agent'), ('lead_agronomist', 'Lead Agronomist'), ('manager', 'Manager/Staff')])

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username','role', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
