from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser, UserProfile, Farm, Crop, Resource, Person
from django.core.validators import MaxValueValidator, MinValueValidator

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
    role = forms.ChoiceField(choices=[('', 'Select a Role'),('farmer', 'Farmer'), ('field_agent', 'Field Agent'), ('manager_staff', 'Manager/Staff')],
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['year_of_birth', 'sex', 'photo', 'nin', 'address', 'phone_number']

    # Add validators to individual fields
    year_of_birth = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1900), MaxValueValidator(2023)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year of Birth'})
    )

    sex = forms.ChoiceField(
        choices=[('Female', 'Female'), ('Male', 'Male')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sex'})
    )

    photo = forms.ImageField(required=False, 
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Upload a Profile Photo'
                             )

    nin = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National Identification Number'})
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3, 'cols': 40})
    )

    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'district', 'location_coordinates', 'land_size', 'crops', 'resources_supplied', 'crop_peelers', 'staff_contacts']

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm Name'})
    )

    district = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'})
    )

    location_coordinates = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location Coordinates'})
    )

    land_size = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Land Size'})
    )

    crops = forms.ModelMultipleChoiceField(
        queryset=Crop.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Crops'})
    )

    resources_supplied = forms.ModelMultipleChoiceField(
        queryset=Resource.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Resources Supplied'})
    )

    crop_peelers = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Crop Peelers'})
    )

    staff_contacts = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Staff'})
    )
