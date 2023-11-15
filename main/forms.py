from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import CustomUser, UserProfile, Farm, Crop, Resource, Person, CropInformation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _


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
        fields = ['district', 'location_coordinates', 'land_size', 'crops']

    district = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District(Lango, Teso, Abim, & Nakaseke)'})
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

    crops = forms.ChoiceField(
        choices=[('', 'Select Crop')],  # Initial empty choice
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Crop'}),
    )
    def __init__(self, *args, **kwargs):
        # Extract 'user' from kwargs
        user = kwargs.pop('user', None)

        # Call the parent __init__ method
        super().__init__(*args, **kwargs)

        # Save 'user' as an attribute of the form
        self.user = user

        # Fetch available crop choices from the database
        crop_choices = Crop.objects.values_list('name', 'name')
        # Add an empty choice for the default placeholder
        crop_choices = [('', 'Select Crop')] + list(crop_choices)

        # Set the choices for the 'crops' field
        self.fields['crops'] = forms.ChoiceField(
            choices=crop_choices,
            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Crop'}),
        )

    def save(self, commit=True):
        farm = super().save(commit=False) 

        # Set the user field
        farm.user = self.user

        # Set the farm name based on user's first name, last name, selected crop, and 'Farm'
        crop_name = self.cleaned_data['crops']
        farm.name = f"{self.user.first_name} {self.user.last_name} {crop_name} Farm"

        if commit:
            farm.save()

        return farm
    
class CropInformationForm(forms.ModelForm):

    date_planting = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
            ))
    
    date_ploughing = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
            ))

    date_weeding = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
            ))


    date_harvesting = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}))
   
    date_fertilizer_application = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}))
    
    
    quantity_planted = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,  
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity Planted'}))
    
    date_fertilizer_application = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    cost_fertilizer_application = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Fertilizer Application'}))
    
    cost_planting = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Planting'}))
    cost_ploughing = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Ploughing'}))
    cost_weeding = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Cost of Weeding'}))
    cost_harvesting = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Harvesting'}))
    
    batch_number = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch Number'}))
    bags_packed = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bags Packed'}))
    
    amount_sold = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Sold'}))
    price_rate = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per Bag'}))
    market = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Market'}))
    
    transport_costs = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Transport Costs'}))
    other_costs = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Other Costs'}))
    
    crop_peelers = ModelMultipleChoiceField(queryset=Person.objects.all(), required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Select Crop Peelers'}))
    
    class Meta:
        model = CropInformation
        fields = ['date_planting', 'date_ploughing', 'date_weeding', 'date_harvesting',
          'quantity_planted', 'date_fertilizer_application', 'cost_fertilizer_application',
          'cost_ploughing', 'cost_weeding', 'cost_harvesting', 'batch_number', 'bags_packed',
          'amount_sold', 'price_rate', 'market', 'transport_costs', 'other_costs',
          'crop_peelers']

        def clean(self):
            cleaned_data = super().clean()
            date_planting = cleaned_data.get('date_planting')
            date_harvesting = cleaned_data.get('date_harvesting')
            quantity_planted = cleaned_data.get('quantity_planted')
            bags_packed = cleaned_data.get('bags_packed')
            amount_sold = cleaned_data.get('amount_sold')
            price_rate = cleaned_data.get('price_rate')

            if date_planting and date_harvesting:
                if date_harvesting < date_planting:
                    raise forms.ValidationError('Harvesting date must be after planting date.')
            
            # Custom validation for date_harvesting and date_planting
            if date_planting and date_harvesting:
                if date_harvesting < date_planting:
                    raise ValidationError(_('Harvesting date must be after planting date.'))

            # Additional validations for quantity_planted, bags_packed, amount_sold, and price_rate
            if quantity_planted and quantity_planted <= 0:
                raise ValidationError(_('Quantity planted must be greater than zero.'))

            if bags_packed and bags_packed < 0:
                raise ValidationError(_('Bags packed cannot be negative.'))

            if amount_sold and amount_sold < 0:
                raise ValidationError(_('Amount sold cannot be negative.'))

            if price_rate and price_rate <= 0:
                raise ValidationError(_('Price rate must be greater than zero.'))

            return cleaned_data
