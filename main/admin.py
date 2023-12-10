from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmingDates,FarmingCosts, FarmProduce, FarmVisitRequest, Message
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from datetime import date


# Register your models here. 

admin.site.register(Crop)
admin.site.register(Farm)
admin.site.register(Person)
admin.site.register(FarmingDates)
admin.site.register(FarmingCosts)
admin.site.register(FarmProduce)
admin.site.register(Resource)
admin.site.register(FarmVisitRequest)
admin.site.register(Message)

# Customize Admin App

admin.site.site_header = 'Windwood Farm Management'
admin.site.site_title = 'Windwood Farm Management'
admin.site.index_title = 'Windwood Farm Management'

class CustomUserAdmin(UserAdmin):
     
     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Add groups to the list filter
     list_filter = ('groups',)

admin.site.register(CustomUser, CustomUserAdmin)

# class CreatedDateFilter(admin.SimpleListFilter):
#     title = 'Created Date'
#     parameter_name = 'created_date'

#     def lookups(self, request, model_admin):
#         return (
#             ('today', 'Today'),
#             ('this_week', 'This week'),
#             ('this_month', 'This month'),
#             ('this_year', 'This year'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'today':
#             return queryset.filter(created__date=date.today())
#         elif self.value() == 'this_week':
#             return queryset.filter(created__week=date.today().isocalendar()[1], created__year=date.today().year)
#         elif self.value() == 'this_month':
#             return queryset.filter(created__month=date.today().month, created__year=date.today().year)
#         elif self.value() == 'this_year':
#             return queryset.filter(created__year=date.today().year)

# class YourModelAdmin(admin.ModelAdmin):
#     list_filter = (CreatedDateFilter,)
#     # ... other configurations ...

# admin.site.register(FarmVisitRequest, CustomUserAdmin)
