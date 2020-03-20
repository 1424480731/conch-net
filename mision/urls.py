from django.contrib import admin
from django.urls import path
from mision import views
app_name='mision'

urlpatterns =[
    path('home/',views.home,name='home'),
    path('upToDateRent/',views.upToDateRent,name='upToDateRent'),
    path('search/',views.search,name='search'),
    path('page/',views.page,name='page'),
    path('location/',views.location,name='location'),
    path('road/',views.road,name='road'),
    path(r'view_fy/<id>/',views.view_fy,name='view_fy'),
]


