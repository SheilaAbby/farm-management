from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('index', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('farmer_home/', views.farmer_home, name='farmer_home'),
    path('field_agent_home/', views.field_agent_home, name='field_agent_home'),
    path('lead_agronomist_home/', views.lead_agronomist_home, name='lead_agronomist_home'),
    path('manager_home/', views.manager_home, name='manager_home'),
    path('password_reset/', views.reset_password, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]