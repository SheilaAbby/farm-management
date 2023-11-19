from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, UserProfileForm, FarmForm, PersonForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Farm, Person
from .forms import FarmForm, CropInformationForm,  PersonForm


# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, 'main/index.html')

@login_required(login_url="/login")
def farmer_home(request):
    user = request.user 
    farms = Farm.objects.filter(user=user)
 
    return render(request, 'main/farmer_home.html', {'user': user, 'farms': farms})

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
            messages.success(request, 'User created successfully. Please log in.')
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

@login_required(login_url="/login")
def update_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    msg = None

    if request.method == 'POST':
        user_form = RegisterForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            print('BOTH SAVED hERE')
            user_form.save()
            profile_form.save()
            msg = 'Profile updated successfully!'
            messages.success(request, 'Profile Updated Successfully!')
            print('BOTH SAVED')
            return redirect('profile') 
        else:
            msg = 'Error Validating Form'
    else:
        user_form = RegisterForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'main/update_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'msg': msg})

@login_required(login_url="/login")
def profile(request):
    return render(request, 'main/profile.html')

@login_required(login_url="/login")
def add_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST, user=request.user)
        if form.is_valid():
            # Save the form data to create a new farm
            new_farm = form.save()
            messages.success(request, 'Farm created successfully')
            return redirect('farmer_home')  # Redirect to farm detail view
    else:
        form = FarmForm(user=request.user)

    return render(request, 'main/add_farm.html', {'form': form})

@login_required(login_url="/login")
def edit_farm(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('farmer_home')
    else:
        form = FarmForm(instance=farm, user=request.user)

    return render(request, 'main/edit_farm.html', {'form': form, 'farm': farm})

@login_required(login_url="/login")
def farm_details(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    # You may add more context data based on your Farm model fields
    return render(request, 'main/farm_details.html', {'farm': farm})

@login_required(login_url="/login")
def create_crop_information(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)

    if request.method == 'POST':
        form = CropInformationForm(request.POST)
        if form.is_valid():
            crop_information = form.save(commit=False)
            crop_information.farm = farm
            crop_information.save()

            messages.success(request, 'Farming Activities Updated Successfully!')
            return redirect('farm_details', farm_id=farm_id)

    else:
        form = CropInformationForm()

    return render(request, 'main/update_crop_info.html', {'farm': farm, 'form': form})

def add_person(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()

            # Add the person to the appropriate relation based on the context (peeling or staff)
            if form.cleaned_data.get('is_peeler'):
                farm.crop_peelers.add(person)
            if form.cleaned_data.get('is_staff'):
                farm.staff_contacts.add(person)

            messages.success(request, 'Person created successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = PersonForm()

    return render(request, 'main/add_person.html', {'form': form, 'farm': farm})

def edit_person(request, farm_id, person_id):
    farm = get_object_or_404(Farm, id=farm_id)
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = PersonForm(instance=person)

    return render(request, 'your_app/edit_person.html', {'form': form, 'farm': farm, 'person': person})

def edit_person(request, farm_id, person_id):
    farm = get_object_or_404(Farm, id=farm_id)
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Person updated successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = PersonForm(instance=person)

    return render(request, 'main/edit_person.html', {'form': form, 'farm': farm, 'person': person})


