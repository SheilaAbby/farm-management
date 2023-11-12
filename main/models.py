from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    # Add additional fields as needed
    role = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    year_of_birth = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    nin = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Person(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_employment = models.DateField(null=True, blank=True)
    
class Farm(models.Model):
    name = models.CharField(max_length=255)
    pictures = models.ManyToManyField('FarmImage', related_name='farms_images', blank=True)
    district = models.CharField(max_length=255)
    location_coordinates = models.CharField(max_length=255)
    crops = models.ManyToManyField('Crop', related_name='farms')
    land_size = models.DecimalField(max_digits=10, decimal_places=2)
    resources_supplied = models.ManyToManyField('Resource', related_name='farms', blank=True)
    
    crop_peelers = models.ManyToManyField('Person', related_name='farms_peeling', blank=True)
    staff_contacts = models.ManyToManyField('Person', related_name='farms_staff', blank=True)

class Crop(models.Model):
    name = models.CharField(max_length=255)

class CropInformation(models.Model):
    crop = models.ForeignKey('Crop', on_delete=models.CASCADE, related_name='crop_information')
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='crop_information')
    
    date_planting = models.DateField(null=True, blank=True)
    date_ploughing = models.DateField(null=True, blank=True)
    date_weeding = models.DateField(null=True, blank=True)
    date_harvesting = models.DateField(null=True, blank=True)
    
    crop_variety = models.CharField(max_length=255, null=True, blank=True)
    quantity_planted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    date_fertilizer_application = models.DateField(null=True, blank=True)
    cost_fertilizer_application = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    cost_planting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_ploughing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_weeding = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_harvesting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    batch_number = models.CharField(max_length=255, null=True, blank=True)
    bags_packed = models.IntegerField(null=True, blank=True)
    
    amount_sold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market = models.CharField(max_length=255, null=True, blank=True)
    
    transport_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    crop_peelers = models.ManyToManyField('Person', blank=True, related_name='peeling_information')
    staff_contacts = models.ManyToManyField('Person', blank=True, related_name='staff_information')

    def clean(self):
        if self.date_harvesting and self.date_planting:
            if self.date_harvesting < self.date_planting:
                raise ValidationError(_('Harvesting date must be after planting date.'))

class Resource(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    date_supplied = models.DateField(null=True, blank=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} units"
    
class FarmImage(models.Model):
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='farm_images/')


