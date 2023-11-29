from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import CustomUser, Farm, Crop, Resource, Person, FarmingDates, FarmingCosts, FarmProduce
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Enter your email address.', 
                             widget = forms.TextInput(
                                 attrs = {"class": "form-control", "placeholder": "Email (to be associated with your account)"}))
    full_name = forms.CharField(max_length=60, help_text='Required. Enter your full name.',
                                 widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "First Name"}))
    username = forms.CharField(max_length=30, help_text='Required. Enter a Username.',
                                widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "Username"}))
  
    birth_year = forms.IntegerField(help_text='Required. Enter your year of birth.',
                                    validators=[MinValueValidator(1900), MaxValueValidator(2023)],
                                    widget=forms.NumberInput(
                                        attrs={"class": "form-control", "placeholder": "Year of Birth"}
                                    ))

    gender = forms.ChoiceField(choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')],
                               widget=forms.Select(
                                   attrs={"class": "form-control"}
                               ))

    national_id = forms.CharField(max_length=20, help_text='Required. Enter your national identification number.',
                                  widget=forms.TextInput(
                                      attrs={"class": "form-control", "placeholder": "National ID", }
                                  ))

    phone_number = forms.CharField(max_length=15, help_text='Required. Enter your phone number.',
                                   widget=forms.TextInput(
                                       attrs={"class": "form-control", "placeholder": "Phone Number"}
                                   ))
    
    phone_belongs_to_user = forms.ChoiceField(choices=[('', 'This is mine ?'),('Yes', 'Yes'), ('No', 'No')],
                             widget = forms.Select(
                                 attrs = {"class": "form-control", "id": "phone_belongs_to_user"}))
    
    # Additional field to hold text when phone number doesn't belong to the user
    phone_number_owner = forms.CharField(max_length=255, required=False,
                                       widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Relationship with the owner ?"}))
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Set the widget attributes for password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'username', 'birth_year', 'gender', 'national_id', 'phone_number', 'phone_belongs_to_user', 'password1', 'password2']

    # Add autocomplete attribute to form fields
    widgets = {
        'email': forms.EmailInput(attrs={'autocomplete': 'email username'}) 
    }

class CustomUserUpdateForm(UserChangeForm):
    # Additional fields not in the CustomUser model
    photo = forms.ImageField(required=False, 
                             widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                             label='Upload a Profile Photo'
                             )
   
    DISTRICT_CHOICES = [
        ('', 'Select District'),
        ('Lango', 'Lango'),
        ('Teso', 'Teso'),
        ('Abim', 'Abim'),
        ('Nakaseke', 'Nakaseke'),
        ('Other', 'Other'),
    ]

    district = forms.ChoiceField(choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    other_location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Location', 'style': 'display:none;'}))
  
    email = forms.EmailField(max_length=254, help_text='Required. Enter your email address.', 
                             widget = forms.TextInput(
                                 attrs = {"class": "form-control", "placeholder": "Email (to be associated with your account)"}))

    username = forms.CharField(max_length=30, help_text='Required. Enter a Username.',
                                widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "Username"}))

    birth_year = forms.IntegerField(help_text='Required. Enter your year of birth.',
                                    validators=[MinValueValidator(1900), MaxValueValidator(2023)],
                                    widget=forms.NumberInput(
                                        attrs={"class": "form-control", "placeholder": "Year of Birth"}
                                    ))

    phone_number = forms.CharField(max_length=15, help_text='Required. Enter your phone number.',
                                   widget=forms.TextInput(
                                       attrs={"class": "form-control", "placeholder": "Phone Number"}
                                   ))
    
    phone_belongs_to_user = forms.ChoiceField(choices=[('', 'Yours ?'),('Yes', 'Yes'), ('No', 'No')],
                             widget = forms.Select(
                                 attrs = {"class": "form-control"}))
    
    farmer_orgs = forms.CharField(max_length=200,required=False,
                                widget = forms.TextInput(
                                    attrs = {"class": "form-control", "placeholder": "Farmer Associations"}))
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'birth_year', 'phone_number', 'phone_belongs_to_user', 'photo', 'district', 'other_location','farmer_orgs']

    def clean(self):
        cleaned_data = super().clean()
        district = cleaned_data.get('district')
        other_location = cleaned_data.get('other_location')

        # Validate that 'other_location' is provided if 'Other' is selected
        if district == 'Other' and not other_location:
            raise forms.ValidationError("Please provide an 'Other' location.")

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "type": "text",
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

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['district', 'other_location', 'location_coordinates', 'land_size', 'crops', 'farm_photo', 'other_crops']

    DISTRICT_CHOICES = [
        ('', 'Select District'),
        ('Lango', 'Lango'),
        ('Teso', 'Teso'),
        ('Abim', 'Abim'),
        ('Nakaseke', 'Nakaseke'),
        ('Other', 'Other'),
    ]

    district = forms.ChoiceField(choices=DISTRICT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_location = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Location', 'style': 'display:none;'}))

    location_coordinates = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location Coordinates'})
    )

    land_size = forms.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Land Size (in acres)'})
    )

    crops = forms.ChoiceField(
        choices=[('', 'Select Crop')],  # Initial empty choice
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Crop'}),
    )

    other_crops = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Crops on the Farm'}))

    farm_photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), label='Upload Farm Photo')
    
    def __init__(self, *args, **kwargs):
        # Extract 'user' from kwargs
        user = kwargs.pop('user', None)

        # Call the parent __init__ method
        super().__init__(*args, **kwargs)
        self.fields['other_location'].required = False

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
        farm.name = f"{self.user.full_name} {crop_name} Farm"

        if commit:
            farm.save()

        return farm
    
    def clean(self):
        cleaned_data = super().clean()
        district = cleaned_data.get('district')
        other_location = cleaned_data.get('other_location')

        # Validate that 'other_location' is provided if 'Other' is selected
        if district == 'Other' and not other_location:
            raise forms.ValidationError("Please provide an 'Other' location.")

        return cleaned_data

class FarmingDatesForm(forms.ModelForm):

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
    
    date_fertilizer_application = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    class Meta:
        model = FarmingDates
        fields = ['date_planting', 'date_ploughing', 'date_weeding', 'date_harvesting', 'date_fertilizer_application']

        def clean(self):
            cleaned_data = super().clean()
            date_planting = cleaned_data.get('date_planting')
            date_harvesting = cleaned_data.get('date_harvesting')

            if date_planting and date_harvesting:
                if date_harvesting < date_planting:
                    raise forms.ValidationError('Harvesting date must be after planting date.')
            
            return cleaned_data

class FarmingCostsForm(forms.ModelForm):

    cost_fertilizer_application = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Cost of Fertilizer App.'}))
    
    cost_planting = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Planting'}))
    cost_ploughing = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Ploughing'}))
    cost_weeding = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Cost of Weeding'}))
    cost_harvesting = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of Harvesting'}))
    transport_costs = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Transport Costs'}))
    other_costs = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Other Costs'}))
    
    class Meta:
        model = FarmingCosts
        fields = ['cost_fertilizer_application','cost_ploughing', 'cost_weeding', 'cost_harvesting']

                 
class FarmProduceForm(forms.ModelForm):

    quantity_planted = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,  
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity Planted'}))
 
   
    batch_number = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Batch Number'}))
    bags_packed = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bags Packed'}))
    amount_sold = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Sold'}))
    price_rate = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per Bag'}))
    market = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Market'}))

    class Meta:
        model = FarmProduce
        fields = ['quantity_planted', 'batch_number', 'bags_packed',
          'amount_sold', 'price_rate', 'market']

        def clean(self):
            cleaned_data = super().clean()
            quantity_planted = cleaned_data.get('quantity_planted')
            bags_packed = cleaned_data.get('bags_packed')
            amount_sold = cleaned_data.get('amount_sold')
            price_rate = cleaned_data.get('price_rate')

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

class PersonForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), label='Upload a Profile Photo')

    class Meta:
        model = Person
        fields = ['photo', 'name', 'phone_number', 'date_of_employment', 'is_peeler', 'is_staff']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_employment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_peeler': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['is_peeler'].label = 'Is A Peeler'
        self.fields['is_staff'].label = 'Is A Staff'

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'quantity', 'date_supplied', 'supplier_name', 'supplier_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource Name'}),
            'date_supplied': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the Supplier'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity Received'}),
            'supplier_phone':forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"})
        }

    def clean_date_supplied(self):
        date_supplied = self.cleaned_data['date_supplied']

        # Check if the date supplied is not in the future
        if date_supplied and date_supplied > timezone.now().date():
            raise ValidationError('Date supplied cannot be in the future.')

        return date_supplied

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        # Check if the quantity is non-negative
        if quantity < 0:
            raise ValidationError('Quantity should be a non-negative number.')

        return quantity