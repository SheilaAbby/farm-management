from django.contrib import admin
from .models import CustomUser, Person, Farm, Crop, Resource, FarmingDates,FarmingCosts, FarmProduce, FarmVisitRequest, Message, FarmVisitReport, Reply
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from datetime import date
from django.utils.translation import gettext_lazy as _

admin.site.register(Crop)

# Customize Admin App

admin.site.site_header = 'Windwood Farm Management'
admin.site.site_title = 'Windwood Farm Management'
admin.site.index_title = 'Windwood Farm Management'


class CreatedDateFilter(admin.SimpleListFilter):
    title = _('Created Date')
    parameter_name = 'created_date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('this_week', _('This week')),
            ('this_month', _('This month')),
            ('this_year', _('This year')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created__date=date.today())
        elif self.value() == 'this_week':
            return queryset.filter(created__week=date.today().isocalendar()[1], created__year=date.today().year)
        elif self.value() == 'this_month':
            return queryset.filter(created__month=date.today().month, created__year=date.today().year)
        elif self.value() == 'this_year':
            return queryset.filter(created__year=date.today().year)


class CreatedDateFilterAdminMixin(admin.ModelAdmin):
    list_filter = (CreatedDateFilter,)

class CreatedDateAndGroupsFilter(admin.SimpleListFilter):
    title = 'Date Joined and Groups'
    parameter_name = 'created_date_and_groups'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This week'),
            ('this_month', 'This month'),
            ('this_year', 'This year'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'today':
            queryset = queryset.filter(date_joined__date=date.today())
        elif value == 'this_week':
            queryset = queryset.filter(date_joined__week=date.today().isocalendar()[1], date_joined__year=date.today().year)
        elif value == 'this_month':
            queryset = queryset.filter(date_joined__month=date.today().month, date_joined__year=date.today().year)
        elif value == 'this_year':
            queryset = queryset.filter(date_joined__year=date.today().year)

        # Handle the groups filter
        groups_value = request.GET.get('groups', None)
        if groups_value:
            queryset = queryset.filter(groups__id=groups_value)

        return queryset

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = (CreatedDateAndGroupsFilter, 'groups')

# Register your CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Farm)
class FarmAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(Person)
class PersonAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(FarmingDates)
class FarmingDatesAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(FarmingCosts)
class FarmingCostsAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(FarmProduce)
class FarmProduceAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(Resource)
class ResourceAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(FarmVisitRequest)
class FarmVisitRequestAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(Message)
class MessageAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(FarmVisitReport)
class FarmVisitReportAdmin(CreatedDateFilterAdminMixin):
    pass

@admin.register(Reply)
class ReplyAdmin(CreatedDateFilterAdminMixin):
    pass
