from django.contrib import admin
from django.urls import path, include
from app import views
from .views import register,login,logout,upload,home

# urlpatterns = [
    #path ('', views.home, name ='home'),
    #path ('register', views.register, name= register),
   # path ('login', views.login, name= login),
    #path ('logout', views.logout, name= logout),
    #path ('upload', views.upload, name= upload),


