from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmingDates,FarmingCosts, FarmProduce, FarmVisitRequest
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Crop)
admin.site.register(Farm)
admin.site.register(Person)
admin.site.register(FarmingDates)
admin.site.register(FarmingCosts)
admin.site.register(FarmProduce)
admin.site.register(Resource)
admin.site.register(FarmVisitRequest)

# Customize Admin App

admin.site.site_header = 'Windwood Farm Management'
admin.site.site_title = 'Windwood Farm Management'
admin.site.index_title = 'Windwood Farm Management'

class CustomUserAdmin(UserAdmin):
     
     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Add groups to the list filter
     list_filter = ('groups',)

admin.site.register(CustomUser, CustomUserAdmin)
