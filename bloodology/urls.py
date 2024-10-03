from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('addRequest',views.AddRequestForm,name='addRequest'),
    path('allRepPost',views.all_posts,name='allRepPost'),
    path('signUp',views.user_signUp,name='signUp'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('search',views.search,name='search'),
    path('profile',views.user_profile,name='profile'),
    path('All_Donors',views.all_Donors,name='All_Donors'),
    path('AboutBdonation',views.AboutBdonation,name='AboutBdonation'),
    path('deleteProfile/<int:id>/',views.deleteProfile, name="deleteProfile"),
    path('<int:id>/',views.updateProfile, name="updateProfile"),
]
