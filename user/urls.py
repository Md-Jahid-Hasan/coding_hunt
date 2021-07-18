from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('details/', views.account_details, name='details'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_details'),
]