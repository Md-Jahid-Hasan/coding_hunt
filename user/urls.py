from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('details/', views.account_details, name='details'),
]