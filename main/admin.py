from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmingDates,FarmingCosts, FarmProduce
from django.contrib.auth.admin import UserAdmin

# Register your models here.

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

class CustomUserAdmin(UserAdmin):
    list_filter = ('role',)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Customize the queryset based on the roles you want to include
        queryset = queryset.exclude(role__in=['lead_agronomist'])

        return queryset, use_distinct

admin.site.register(CustomUser, CustomUserAdmin)
