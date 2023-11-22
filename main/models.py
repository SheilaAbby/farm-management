from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):
    # Add additional fields as needed
    role = models.CharField(max_length=50)
    birth_year = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    phone_belongs_to_user = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='no')
    full_name = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def age(self):
        from datetime import date
        if self.birth_year:
            today = date.today()
            return today.year - self.birth_year
        return None

    @property
    def has_farm(self):
        # Check if the user has an associated farm
        return self.farm_set.exists()  

class Person(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_employment = models.DateField(null=True, blank=True)
    is_peeler = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    
class Crop(models.Model):
    CROP_CHOICES = [
        ('Cassava', 'Cassava 🍠'),
        ('Maize', 'Maize 🌽'),
        ('Rice', 'Rice 🍚'),
    ]

    name = models.CharField(max_length=255, choices=CROP_CHOICES)

    def __str__(self):
        return self.name
    
class Farm(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    crops = models.CharField(max_length=255)
    pictures = models.ManyToManyField('FarmImage', related_name='farms_images', blank=True)
    district = models.CharField(max_length=255)
    location_coordinates = models.CharField(max_length=255)
    land_size = models.DecimalField(max_digits=10, decimal_places=2)
    resources_supplied = models.ManyToManyField('Resource', related_name='farms', blank=True)
    
    crop_peelers = models.ManyToManyField('Person', related_name='farms_peeling', blank=True)
    staff_contacts = models.ManyToManyField('Person', related_name='farms_staff', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FarmingDates(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='farming_dates')
    date_planting = models.DateField(null=True, blank=True)
    date_ploughing = models.DateField(null=True, blank=True)
    date_weeding = models.DateField(null=True, blank=True)
    date_harvesting = models.DateField(null=True, blank=True)
    date_fertilizer_application = models.DateField(null=True, blank=True)
    models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

class FarmingCosts(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='farming_costs')
    cost_planting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_ploughing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_weeding = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_harvesting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transport_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
  
class FarmProduce(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='farm_produce')
    quantity_planted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    batch_number = models.CharField(max_length=255, null=True, blank=True)
    bags_packed = models.IntegerField(null=True, blank=True)
    amount_sold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

class Resource(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    date_supplied = models.DateField(null=True, blank=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_phone = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.quantity} units"
    
class FarmImage(models.Model):
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='farm_images/')


