from django.urls import path, re_path
from .views import react_fronted

app_name = 'frontend'
urlpatterns = [
    path('', react_fronted, name='react_frontend'),

]