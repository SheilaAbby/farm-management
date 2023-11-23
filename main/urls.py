from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('index', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('sign-up/', views.sign_up, name='custom_signup'),
    path('farmer_home/', views.farmer_home, name='farmer_home'),
    path('field_agent_home/', views.field_agent_home, name='field_agent_home'),
    path('lead_agronomist_home/', views.lead_agronomist_home, name='lead_agronomist_home'),
    path('manager_home/', views.manager_home, name='manager_home'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('add_farm/', views.add_farm, name='add_farm'),
    path('edit_farm/<int:farm_id>/', views.edit_farm, name='edit_farm'),
    path('farm_details/<int:farm_id>/', views.farm_details, name='farm_details'),
    path('add_person/<int:farm_id>/farm_workers', views.add_person, name='add_person'),
    path('edit_person/<int:farm_id>/<int:person_id>/', views.edit_person, name='edit_person'),
    path('farm/<int:farm_id>/add_farm_dates/', views.add_farm_dates, name='add_farm_dates'),
    path('farm/<int:farm_id>/update_farm_dates/<int:farming_dates_id>/', views.update_farm_dates, name='update_farm_dates'),
    path('farm/<int:farm_id>/add_farm_costs/', views.add_farm_costs, name='add_farm_costs'),
    path('farm/<int:farm_id>/update_farm_costs/', views.update_farm_costs, name='update_farm_costs'),
    path('farm/<int:farm_id>/add_farm_produce/', views.add_farm_produce, name='add_farm_produce'), 
    path('farm/<int:farm_id>/update_farm_produce/', views.update_farm_produce, name='update_farm_produce'),
    path('<int:farm_id>/view_more_farm_dates/', views.view_more_farm_dates, name='view_more_farm_dates'),
    path('<int:farm_id>/view_more_farm_costs/', views.view_more_farm_costs, name='view_more_farm_costs'),
    path('<int:farm_id>/view_more_farm_produce/', views.view_more_farm_produce, name='view_more_farm_produce'),
    path('<int:farm_id>/view_more_farm_staff/', views.view_more_farm_staff, name='view_more_farm_staff'),

# Password Reset urls
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
 # Include media URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)