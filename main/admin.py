from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmingDates,FarmingCosts, FarmProduce

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Crop)
admin.site.register(Farm)
admin.site.register(Person)
admin.site.register(FarmingDates)
admin.site.register(FarmingCosts)
admin.site.register(FarmProduce)
admin.site.register(Resource)

# Customize Admin App

admin.site.site_header = 'Windwood Farm Management'
admin.site.site_title = 'Windwood Farm Management'
admin.site.index_title = 'Windwood Farm Management'
