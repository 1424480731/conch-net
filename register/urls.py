from django.contrib import admin
from django.urls import path
from register import views
app_name='register'

urlpatterns =[
    path('verifyuser/',views.verify_user_exist,name='verify_user_exist'),
    path('sign_in/',views.sign_in,name='sign_in'),
]




