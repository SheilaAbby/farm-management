from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, CustomUserUpdateForm, FarmForm, PersonForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .models import Farm, Person, FarmingDates, FarmingCosts, FarmProduce
from .forms import FarmForm,  PersonForm, FarmingDatesForm, FarmingCostsForm,FarmProduceForm 


# Create your views here.
@login_required(login_url="/login")
def index(request):
      if request.user.is_authenticated:
        if  request.user.role == 'farmer': 
            return redirect('farmer_home')
        elif request.user.role == 'field_agent':
            return redirect('field_agent_home') 
        elif request.user.role == 'manager_staff':
            return redirect('manager_home')
      else:
          return redirect('login') 

@login_required(login_url="/login")
def farmer_home(request):
    user = request.user 
    farms = Farm.objects.filter(user=user)

    farm_exists = Farm.objects.filter(user=user).exists()
    farm_queryset = Farm.objects.filter(user=user)

    context = {
        'farm_exists': farm_exists,
        'farm_queryset': farm_queryset,
        'user': user,
        'farms': farms
    }
 
    return render(request, 'main/farmer_home.html', context)

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

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=user)
        print('FORM initialized')

        if user_form.is_valid():
            print('FORM VALID')
            user_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            # Debugging: Print form errors to the console
            print("Form Errors:", user_form.errors)
    else:
        user_form = CustomUserUpdateForm(instance=user)

    return render(request, 'main/update_profile.html', {'user_form': user_form})

@login_required(login_url="/login")
def profile(request):
    return render(request, 'main/profile.html')

@login_required(login_url="/login")
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

@login_required(login_url="/login")
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
            return redirect('farm_details', farm_id)
    else:
        form = FarmForm(instance=farm, user=request.user)

    return render(request, 'main/edit_farm.html', {'form': form, 'farm': farm})

@login_required(login_url="/login")
def farm_details(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    # Check if farming dates, farming costs, and farm produce, workers exist for the farm
    farming_dates_exist = FarmingDates.objects.filter(farm=farm).exists()
    farming_costs_exist = FarmingCosts.objects.filter(farm=farm).exists()
    farm_produce_exist = FarmProduce.objects.filter(farm=farm).exists()
    farm_peelers_exist = farm.crop_peelers.exists()
    farm_staff_exist = farm.staff_contacts.exists()
    
    farming_dates_queryset = FarmingDates.objects.filter(farm=farm)
    farming_costs_queryset = FarmingCosts.objects.filter(farm=farm)
    farm_produce_queryset = FarmProduce.objects.filter(farm=farm)
    farm_peelers_queryset = farm.crop_peelers.all()
    farm_staff_queryset = farm.staff_contacts.all()

    context = {
        'farm': farm,
        'farm_id': farm_id,
        'farming_dates_exist': farming_dates_exist,
        'farming_costs_exist': farming_costs_exist,
        'farm_produce_exist': farm_produce_exist,
        'farm_peelers_exist': farm_peelers_exist,
        'farm_staff_exist': farm_staff_exist,
        'farming_dates_queryset': farming_dates_queryset,
        'farming_costs_queryset': farming_costs_queryset,
        'farm_produce_queryset': farm_produce_queryset,
        'farm_peelers_queryset': farm_peelers_queryset,
        'farm_staff_queryset': farm_staff_queryset
    }

    return render(request, 'main/farm_details.html', context)

@login_required(login_url="/login")
def add_farm_dates(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    if request.method == 'POST':
        form = FarmingDatesForm(request.POST)
        if form.is_valid():
            farming_dates = form.save(commit=False)
            farming_dates.farm = farm
            farming_dates.save()
            messages.success(request, 'Farming Dates Submitted Successfully!')
            return redirect('farm_details', farm_id)
    else:
        form = FarmingDatesForm()

    return render(request, 'main/add_farm_dates.html', {'farm': farm, 'form': form, 'farm_id': farm_id})

@login_required(login_url="/login")
def update_farm_dates(request, farm_id, farming_dates_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farming_dates = get_object_or_404(FarmingDates, id=farming_dates_id, farm=farm)

    if request.method == 'POST':
        form = FarmingDatesForm(request.POST, instance=farming_dates)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Dates Updated Successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmingDatesForm(instance=farming_dates)

    return render(request, 'main/update_farm_dates.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farming_dates_id': farming_dates_id})

@login_required(login_url="/login")
def add_farm_costs(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    if request.method == 'POST':
        form = FarmingCostsForm(request.POST)
        if form.is_valid():
            farming_costs = form.save(commit=False)
            farming_costs.farm = farm
            farming_costs.save()
            messages.success(request, 'Farm Costs Submitted Successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmingCostsForm()

    return render(request, 'main/add_farm_costs.html', {'farm': farm, 'form': form, 'farm_id': farm_id})

@login_required(login_url="/login")
def update_farm_costs(request, farm_id, farming_costs_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farming_costs = get_object_or_404(FarmingCosts, id=farming_costs_id, farm=farm)

    if request.method == 'POST':
        form = FarmingCostsForm(request.POST, instance=farming_costs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Costs Updated Successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmingCostsForm(instance=farming_costs)

    return render(request, 'main/update_farm_costs.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farming_costs_id': farming_costs_id})

@login_required(login_url="/login")
def add_farm_produce(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    if request.method == 'POST':
        form = FarmProduceForm(request.POST)
        if form.is_valid():
            farm_produce = form.save(commit=False)
            farm_produce.farm = farm
            farm_produce.save()
            messages.success(request, 'Farm Produce Submitted Successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmProduceForm()

    return render(request, 'main/add_farm_produce.html', {'farm': farm, 'form': form,'farm_id': farm_id})

@login_required(login_url="/login")
def update_farm_produce(request, farm_id, farm_produce_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farm_produce = get_object_or_404(FarmProduce, id=farm_produce_id, farm=farm)

    if request.method == 'POST':
        form = FarmProduceForm(request.POST, instance=farm_produce)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Produce Updated Successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmProduceForm(instance=farm_produce)

    return render(request, 'main/update_farm_produce.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farm_produce_id': farm_produce_id})

@login_required(login_url="/login")
def view_more_farm_dates(request, farm_id):
    # Retrieve all farm dates for the given farm
    all_farm_dates = FarmingDates.objects.filter(farm_id=farm_id)

    # Exclude the first 3 farm dates
    additional_farm_dates = all_farm_dates[3:]

    context = {
        'additional_farm_dates': additional_farm_dates,
        'farm_id': farm_id,
    }

    return render(request, 'main/view_more_farm_dates.html', context)

@login_required(login_url="/login")
def view_more_farm_costs(request, farm_id):
    # Retrieve all farm dates for the given farm
    all_farm_dates = FarmingCosts.objects.filter(farm_id=farm_id)

    # Exclude the first 3 farm dates
    additional_farm_dates = all_farm_dates[3:]

    context = {
        'additional_farm_costs': additional_farm_dates,
        'farm_id': farm_id,
    }

    return render(request, 'main/view_more_farm_costs.html', context)

@login_required(login_url="/login")
def view_more_farm_produce(request, farm_id):
    # Retrieve all farm dates for the given farm
    all_farm_dates = FarmProduce.objects.filter(farm_id=farm_id)

    # Exclude the first 3 farm dates
    additional_farm_dates = all_farm_dates[3:]

    context = {
        'additional_farm_produce': additional_farm_dates,
        'farm_id': farm_id,
    }

    return render(request, 'main/view_more_farm_produce.html', context)

@login_required(login_url="/login")
def view_more_farm_staff(request, farm_id):
    # Retrieve all farm staff for the given farm
    farm = get_object_or_404(Farm, id=farm_id)
    staff_members = farm.staff_contacts.all()

    # Exclude the first 2 staff
    additional_farm_staff = staff_members[2:]

    context = {
        'additional_farm_staff': additional_farm_staff,
        'farm_id': farm_id,
    }

    return render(request, 'main/view_more_farm_staff.html', context)
