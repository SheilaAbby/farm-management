from django.db.models import Q
from django.http import HttpResponse, JsonResponse
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm, CustomUserUpdateForm, FarmForm, PersonForm, RegisterForm, FarmPhotoForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Farm, Person, FarmingDates, FarmingCosts, FarmProduce, Resource, FarmVisitRequest
from .forms import FarmForm,  PersonForm, FarmingDatesForm, FarmingCostsForm,FarmProduceForm, ResourceForm, FarmVisitRequestForm
from main.models import CustomUser 


def is_farmer_or_field_agent(user):
    return user.groups.filter(name__in=['farmer', 'field_agent']).exists()

@user_passes_test(is_farmer_or_field_agent)
def index(request):
    if request.user.is_authenticated:
        # Redirect to appropriate view based on user group
        if 'farmer' in request.user.groups.values_list('name', flat=True):
            return redirect('farmer_home')
        elif 'field_agent' in request.user.groups.values_list('name', flat=True):
            return redirect('farmer_home')
    else:
        return redirect('login') 
      
@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def farmer_home(request):
    user = request.user 
    farms = Farm.objects.filter(user=user)
    farms = Farm.objects.filter(user=user)
    is_field_agent = user.groups.filter(name='field_agent').exists()
    farms_in_agent_district = Farm.objects.filter(Q(district=user.district)).order_by('-created')[:5]

    farm_exists = Farm.objects.filter(user=user).exists()
    farm_queryset = Farm.objects.filter(user=user)

    latest_user_farms = Farm.objects.filter(user=user).order_by('-created')[:5]

    context = {
        'farm_exists': farm_exists,
        'farm_queryset': farm_queryset,
        'user': user,
        'farms': farms,
        'is_field_agent': is_field_agent,
        'farms_in_agent_district': farms_in_agent_district,
        'latest_user_farms': latest_user_farms
    }
 
    return render(request, 'main/farmer_home.html', context)

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
            
            if user is not None:
                if user.groups.filter(name='farmer').exists():
                    login(request, user)
                    return redirect('farmer_home')
                elif user.groups.filter(name='field_agent').exists():
                    login(request, user)
                    return redirect('farmer_home')
                elif user.groups.filter(name='manager_staff').exists():
                    login(request, user)
                    return redirect('manager_home')
                else:
                    msg = 'Account does not belong to a valid group. Please Check with the Site Admin'
            else:
                msg = 'Invalid username or password. Please try again.'
        else:
            msg = 'Error Validating Form'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})

@login_required(login_url="/login")
def custom_logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login')) 

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
    else:
        user_form = CustomUserUpdateForm(instance=user)

    return render(request, 'main/update_profile.html', {'user_form': user_form, 'user': user})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def profile(request):
    return render(request, 'main/profile.html')

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def add_person(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()

            # Add the person to the appropriate relation based on the context (peeling or staff)
            if form.cleaned_data.get('is_peeler'):
                farm.crop_peelers.add(person)
            if form.cleaned_data.get('is_staff'):
                farm.staff_contacts.add(person)

            messages.success(request, 'Person created successfully!')
            return redirect('farm_workers', farm_id=farm_id)
    else:
        form = PersonForm()

    return render(request, 'main/add_person.html', {'form': form, 'farm': farm})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def delete_person(request, farm_id, person_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Farm Worker Deleted Successfully!')
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer']).exists())
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

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer']).exists())
@login_required(login_url="/login")
def edit_farm(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    if request.method == 'POST':
        form = FarmForm(request.POST, request.FILES, instance=farm, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farm Details updated successfully!')
            return redirect('farm_details', farm_id)
    else:
        form = FarmForm(instance=farm, user=request.user)

    return render(request, 'main/edit_farm.html', {'form': form, 'farm': farm})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def farm_details(request, farm_id):
    user = request.user
    farm = get_object_or_404(Farm, id=farm_id)
    is_field_agent = user.groups.filter(name='field_agent').exists()
    

    # Process farm visit form submission
    if request.method == 'POST':
        form = FarmVisitRequestForm(request.POST)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.requester = user
            visit.farm = farm
            visit.save()
            messages.success(request, 'Farm visit request submitted successfully!')
            return redirect('farm_details', farm_id=farm_id)
    else:
        form = FarmVisitRequestForm()

    farm_visit_requests = FarmVisitRequest.objects.filter(farm=farm)

    context = {
        'farm': farm,
        'farm_id': farm_id,
        'is_field_agent': is_field_agent,
        'farm_visit_requests': farm_visit_requests,
        'form': form,
    }

    return render(request, 'main/farm_details.html', context)

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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
            return redirect('farm_activities', farm_id)
    else:
        form = FarmingDatesForm()

    return render(request, 'main/add_farm_dates.html', {'farm': farm, 'form': form, 'farm_id': farm_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def update_farm_dates(request, farm_id, farming_dates_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farming_dates = get_object_or_404(FarmingDates, id=farming_dates_id, farm=farm)

    if request.method == 'POST':
        form = FarmingDatesForm(request.POST, instance=farming_dates)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Dates Updated Successfully!')
            return redirect('farm_activities', farm_id=farm_id)
    else:
        form = FarmingDatesForm(instance=farming_dates)

    return render(request, 'main/update_farm_dates.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farming_dates_id': farming_dates_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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
            return redirect('farm_activities', farm_id=farm_id)
    else:
        form = FarmingCostsForm()

    return render(request, 'main/add_farm_costs.html', {'farm': farm, 'form': form, 'farm_id': farm_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def update_farm_costs(request, farm_id, farming_costs_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farming_costs = get_object_or_404(FarmingCosts, id=farming_costs_id, farm=farm)

    if request.method == 'POST':
        form = FarmingCostsForm(request.POST, instance=farming_costs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Costs Updated Successfully!')
            return redirect('farm_activities', farm_id=farm_id)
    else:
        form = FarmingCostsForm(instance=farming_costs)

    return render(request, 'main/update_farm_costs.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farming_costs_id': farming_costs_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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
            return redirect('farm_activities', farm_id=farm_id)
    else:
        form = FarmProduceForm()

    return render(request, 'main/add_farm_produce.html', {'farm': farm, 'form': form,'farm_id': farm_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def update_farm_produce(request, farm_id, farm_produce_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    farm_produce = get_object_or_404(FarmProduce, id=farm_produce_id, farm=farm)

    if request.method == 'POST':
        form = FarmProduceForm(request.POST, instance=farm_produce)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farming Produce Updated Successfully!')
            return redirect('farm_activities', farm_id=farm_id)
    else:
        form = FarmProduceForm(instance=farm_produce)

    return render(request, 'main/update_farm_produce.html', {'farm': farm, 'form': form, 'farm_id': farm_id, 'farm_produce_id': farm_produce_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
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

def view_more_farm_peelers(request, farm_id):
    # Retrieve all farm staff for the given farm
    farm = get_object_or_404(Farm, id=farm_id)
    peelers = farm.crop_peelers.all()

    # Exclude the first 2 staff
    additional_farm_peelers = peelers[2:]

    context = {
        'additional_farm_peelers': additional_farm_peelers,
        'farm_id': farm_id,
    }

    return render(request, 'main/view_more_farm_peelers.html', context)

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def create_resource(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.save()
            farm.resources_supplied.add(resource)
            messages.success(request, 'Resource Submitted Successfully!')
            # Redirect to a success page or display a success message
            return redirect('farm_resources', farm_id=farm_id)
    else:
        form = ResourceForm()

    return render(request, 'main/add_resources.html', {'form': form, 'farm_id':farm_id})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
def farm_resources(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    resources = farm.resources_supplied.order_by('-created')

    return render(request, 'main/farm_resources.html', {'farm': farm, 'resources': resources})

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def farm_workers(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    # Check if workers exist for the farm
  
    farm_peelers_exist = farm.crop_peelers.exists()
    farm_staff_exist = farm.staff_contacts.exists()
   
    farm_peelers_queryset = farm.crop_peelers.order_by('-created')
    farm_staff_queryset = farm.staff_contacts.order_by('-created')

    context = {
        'farm': farm,
        'farm_id': farm_id,
        'farm_peelers_exist': farm_peelers_exist,
        'farm_staff_exist': farm_staff_exist,
        'farm_peelers_queryset': farm_peelers_queryset,
        'farm_staff_queryset': farm_staff_queryset
    }

    return render(request, 'main/farm_workers.html', context)

@user_passes_test(lambda u: u.groups.filter(name__in=['farmer', 'field_agent']).exists())
@login_required(login_url="/login")
def farm_activities(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)

    # Check if farming dates, farming costs, and farm produce, workers exist for the farm
    farming_dates_exist = FarmingDates.objects.filter(farm=farm).exists()
    farming_costs_exist = FarmingCosts.objects.filter(farm=farm).exists()
    farm_produce_exist = FarmProduce.objects.filter(farm=farm).exists()
   
    
    farming_dates_queryset = FarmingDates.objects.filter(farm=farm).order_by('-created')
    farming_costs_queryset = FarmingCosts.objects.filter(farm=farm).order_by('-created')
    farm_produce_queryset = FarmProduce.objects.filter(farm=farm).order_by('-created')

    context = {
        'farm': farm,
        'farm_id': farm_id,
        'farming_dates_exist': farming_dates_exist,
        'farming_costs_exist': farming_costs_exist,
        'farm_produce_exist': farm_produce_exist,
        'farming_dates_queryset': farming_dates_queryset,
        'farming_costs_queryset': farming_costs_queryset,
        'farm_produce_queryset': farm_produce_queryset
    }

    return render(request, 'main/farm_activities.html', context)

@login_required(login_url="/login")
def farm_photos(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id)
    media_path = 'media/farm_photos/'
    image_names = [filename for filename in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, filename))]
  
    if request.method == 'POST':
        form = FarmPhotoForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.farm = farm
            photo.uploaded_by = request.user 
            photo.save()
            messages.success(request, 'Farm photo uploaded successfully!')
            return redirect('farm_photos', farm_id=farm_id)
    else:
        form = FarmPhotoForm()

    context = {
        'farm': farm,
        'farm_id': farm_id,
        'form': form,
        'image_names': image_names,
        'media_path': media_path
    }

    return render(request, 'main/farm_photos.html', context)

def get_image_names(request):
    media_path = 'media/farm_photos/'
    image_names = [filename for filename in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, filename))]
    

    return JsonResponse({'image_names': image_names})