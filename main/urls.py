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
    path('farm/<int:farm_id>/update_farm_costs/<int:farming_costs_id>/', views.update_farm_costs, name='update_farm_costs'),
    path('farm/<int:farm_id>/add_farm_produce/', views.add_farm_produce, name='add_farm_produce'), 
    path('farm/<int:farm_id>/update_farm_produce/<int:farm_produce_id>/', views.update_farm_produce, name='update_farm_produce'),
    path('view_more_farms/', views.view_more_farms, name='view_more_farms'),
    path('<int:farm_id>/view_more_farm_dates/', views.view_more_farm_dates, name='view_more_farm_dates'),
    path('<int:farm_id>/view_more_farm_costs/', views.view_more_farm_costs, name='view_more_farm_costs'),
    path('<int:farm_id>/view_more_farm_produce/', views.view_more_farm_produce, name='view_more_farm_produce'),
    path('<int:farm_id>/view_more_farm_staff/', views.view_more_farm_staff, name='view_more_farm_staff'),
    path('<int:farm_id>/view_more_farm_peelers/', views.view_more_farm_peelers, name='view_more_farm_peelers'),
    path('farm/<int:farm_id>/delete_person/<int:person_id>/', views.delete_person, name='delete_person'),
    path('farm_details/<int:farm_id>/create_resource/', views.create_resource, name='create_resource'),
    path('farm_resources/<int:farm_id>/', views.farm_resources, name='farm_resources'),
    path('farm_workers/<int:farm_id>/', views.farm_workers, name='farm_workers'),
    path('farm_activities/<int:farm_id>/', views.farm_activities, name='farm_activities'),
    path('farm/<int:farm_id>/farm_photos/', views.farm_photos, name='farm_photos'),
    path('get_image_names/', views.get_image_names, name='get_image_names'),
    path('search/', views.search_view, name='search_view'),
    path('farm/<int:farm_id>/delete_farm/', views.delete_farm, name='delete_farm'),
    path('fetch_messages/', views.fetch_messages, name='fetch_messages'),
    path('windwood/chatroom/', views.send_message, name='send_message'),

    # Password Reset urls
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
 # Include media URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)