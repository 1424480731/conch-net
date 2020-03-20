from django.contrib import admin
from django.urls import path
from login import views
app_name='login'

urlpatterns =[
    path('login/',views.login,name='login'),
    path('out/',views.out,name='out'),
]
