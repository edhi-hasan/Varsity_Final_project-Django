from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('addRequest',views.AddRequestForm,name='addRequest'),
    path('signUp',views.user_signUp,name='signUp'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('search',views.search,name='search'),
    path('profile',views.user_profile,name='profile'),
    path('AboutBdonation',views.AboutBdonation,name='AboutBdonation'),
]
