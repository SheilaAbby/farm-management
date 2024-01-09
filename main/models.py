from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import os

# Create your models here.
class CustomUser(AbstractUser): 
    
    DISTRICT_CHOICES = [
        ('', 'Select District'),
        ('Lango', 'Lango'),
        ('Teso', 'Teso'),
        ('Abim', 'Abim'),
        ('Nakaseke', 'Nakaseke'),
        ('Other', 'Other'),
    ]

    # Add additional fields as needed
    birth_year = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    national_id = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    phone_belongs_to_user = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='no')
    full_name = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    district = models.TextField(blank=True, null=True, choices=DISTRICT_CHOICES)
    other_location = models.TextField(blank=True, null=True)
    
    # Additional field to hold text when phone number doesn't belong to the user
    phone_number_owner = models.CharField(max_length=255, blank=True, null=True)
    farmer_orgs = models.CharField(max_length=255, blank=True)

    last_checked_message = models.DateTimeField(null=True, blank=True)

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
    
    
    
    def save(self, *args, **kwargs):

       if self.other_location and self.other_location != self.DISTRICT_CHOICES[0][0]:
            # Update district only if it was originally set to 'Other'
            if self.district == self.DISTRICT_CHOICES[-1][0]:
                self.district = self.other_location

       super().save(*args, **kwargs)

    @property
    def processed_messages(self):
        # Retrieve or create ProcessedMessage instance for the user
        processed_message, created = ProcessedMessage.objects.get_or_create(user=self)
        return processed_message
    
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

    DISTRICT_CHOICES = [
        ('', 'Select District'),
        ('Lango', 'Lango'),
        ('Teso', 'Teso'),
        ('Abim', 'Abim'),
        ('Nakaseke', 'Nakaseke'),
        ('Other', 'Other'),
    ]
     
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    crops = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    other_location = models.CharField(max_length=255)
    location_coordinates = models.CharField(max_length=255)
    land_size = models.DecimalField(max_digits=10, decimal_places=2)
    resources_supplied = models.ManyToManyField('Resource', related_name='farms', blank=True)
    
    farm_labourers = models.ManyToManyField('Person', related_name='farms_labourer', blank=True)
    staff_contacts = models.ManyToManyField('Person', related_name='farms_staff', blank=True)
    other_crops = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.name
    
    def get_latest_photos(self, count=5):
        return self.farm_photos.all().order_by('-uploaded_at')[:count]
    
    def get_image_url(self, image_name):
        return os.path.join('farm_photos', str(self.id), image_name)
    def save(self, *args, **kwargs):

       if self.other_location and self.other_location != self.DISTRICT_CHOICES[0][0]:
            # Update district only if it was originally set to 'Other'
            if self.district == self.DISTRICT_CHOICES[-1][0]:
                self.district = self.other_location

       super().save(*args, **kwargs)
    
class Person(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_employment = models.DateField(null=True, blank=True)
    casual_labourer = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False) 
    photo = models.ImageField(upload_to='workers_photos/', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
  
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
    cost_fertilizer_application = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_planting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_ploughing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_weeding = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_harvesting = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transport_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
  
class FarmProduce(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='farm_produce')
    quantity_planted = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    batch_number = models.CharField(max_length=255, null=True, blank=True)
    bags_harvested = models.IntegerField(null=True, blank=True)
    amount_sold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_kgs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_amount_tonnes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    market = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

class Resource(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    date_supplied = models.DateField(null=True, blank=True)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_phone = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.quantity} units"

User = get_user_model()

class FarmVisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
     
    visit_date = models.DateField()
    purpose = models.TextField()
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_visits')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='farm_visits')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Visit to {self.farm} on {self.visit_date} | Submitted On {self.created.strftime('%Y-%m-%d')}"

class FarmVisitReport(models.Model):
    farm_visit_request = models.OneToOneField(
        'FarmVisitRequest',
        on_delete=models.CASCADE,
        related_name='farm_visit_report'
    )
    report = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report for Farm Visit Request {self.farm_visit_request.id} ({self.created.strftime('%Y-%m-%d')})"

class FarmPhoto(models.Model):
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='farm_photos')
    photo = models.ImageField(upload_to='farm_photos/')
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(CustomUser, related_name='received_messages')
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    deleted_for_recipients = models.BooleanField(default=False)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_field_agent = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} Sent on ({self.created.strftime('%Y-%m-%d')})"


class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(User, related_name='sent_replies', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reply Message from {self.sender}, to {self.message}"

class ProcessedMessage(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    processed_message_ids = models.JSONField(default=list)
