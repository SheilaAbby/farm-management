from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UserProfileForm,FarmForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import UserProfile

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
    return render(request, 'registration/custom_signup.html', {'form': form, 'msg': msg})
   
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
            elif user is not None and user.role == 'field_agent':
                login(request, user)
                return redirect('field_agent_home')
            elif user is not None and user.role == 'manager_staff':
                login(request, user)
                return redirect('manager_home')
            else:
                msg = 'Invalid username or password. Please try again.'
        else:
            msg = 'Error Validating Form'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})

@login_required(login_url="/login")
def custom_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login')) 

def update_profile(request):
    # Assuming you have the user instance
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    msg = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            msg = 'user updated'
            # Redirect to their profile page
            return redirect('profile')
        else:
            msg = 'Error Validating Form'
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'main/update_profile.html', {'form': form, 'msg': msg})

def profile(request):
    return render(request, 'main/profile.html')

def add_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new farm
            new_farm = form.save()
            return redirect('farm_detail', pk=new_farm.pk)  # Redirect to farm detail view
    else:
        form = FarmForm()

    return render(request, 'main/add_farm.html', {'form': form})

