from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, PasswordResetForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, 'main/index.html')

@login_required(login_url="/login")
def farmer_home(request):
    return render(request, 'main/farmer_home.html')

@login_required(login_url="/login")
def field_agent_home(request):
    return render(request, 'main/field_agent_home.html')

@login_required(login_url="/login")
def lead_agronomist_home(request):
    return render(request, 'main/lead_agronomist_home.html')

@login_required(login_url="/login")
def manager_home(request):
    return render(request, 'main/manager_home.html')

def sign_up(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect ('login')
        else:
            msg = 'form is invalid'
    else:
            form =  form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form, 'msg': msg})
   
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.role == 'farmer':
                login(request, user)
                return redirect('farmer_home')
            elif user is not None and user.role == 'lead_agronomist':
                login(request, user)
                return redirect('lead_agronomist_home')
            elif user is not None and user.role == 'manager':
                login(request, user)
                return redirect('manager_home')
            else:
                msg = 'Invalid Credentials'
        else:
            msg = 'Error Validating Form'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})

@login_required(login_url="/login")
def custom_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login')) 

def reset_password(request):
    form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {"form": form})
    # if request.method == 'POST':
    #     form = PasswordResetForm(request.POST)
    #     if form.is_valid():
    #         return redirect('/password_reset/done')
    # else:
    #     form = PasswordResetForm()
    # return render(request, 'registration/password_reset_form.html', {"form": form})

    # form_class = PasswordResetForm
    # template_name = 'registration/password_reset_form.html.html'

    # subject = 'Test Email'
    # message = 'This is a test email sent using Mailgun.'
    # from_email = 'postmaster@sandboxeba38c7c567940d392f5335911764c14.mailgun.org'
    # recipient_list = ['sheilakioko@gmail.com']

    # send_mail(subject, message, from_email, recipient_list)

    # return HttpResponse('Email sent successfully.')
