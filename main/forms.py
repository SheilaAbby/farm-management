import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter your email address.', 
                             widget = forms.TextInput(
                                 attrs = {"class": "form-control", "placeholder": "Email"}))
    first_name = forms.CharField(max_length=30, help_text='Required. Enter your first name.',
                                 widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(max_length=30, help_text='Required. Enter your last name.', 
                                widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "Last Name"}))
    username = forms.CharField(max_length=30, help_text='Required. Enter a Username.',
                                widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "Username"}))
    role = forms.ChoiceField(choices=[('', 'Select a Role'),('farmer', 'Farmer'), ('field_agent', 'Field Agent'), ('lead_agronomist', 'Lead Agronomist'), ('manager', 'Manager/Staff')],
                             widget = forms.Select(
                                 attrs = {"class": "form-control"}))
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Set the widget attributes for password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username','role', 'password1', 'password2']

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

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom CSS classes to form elements
        self.fields['email'].widget.attrs['class'] = 'custom-class'