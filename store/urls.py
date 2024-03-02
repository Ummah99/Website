from django.contrib import admin
from django.urls import path
from app import views
from app.views import home, upload, login_user, register, logout,activate
from django.contrib.auth import views as auth
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload, name="upload"),
   # path('', include("django.contrib.auth.urls")),
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/',register, name='register'),
    path('activate/<uidb64>/<token>', activate, name= "activate"),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/pannel1.html'), name='logout'),

   # path('logout/', auth.LogoutView.as_view(template_name ='store/pannel1.html'), name ='logout'),

] 
    
    #path('activate/<uidb64>/<token>', views.activate, name='activate') 