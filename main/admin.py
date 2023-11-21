from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmImage

# Register your models here.

admin.site.register(CustomUser)
# admin.site.register(UserProfile)
admin.site.register(Person)
admin.site.register(Farm)
admin.site.register(Crop)
# admin.site.register(CropInformation)
admin.site.register(Resource)
admin.site.register(FarmImage)