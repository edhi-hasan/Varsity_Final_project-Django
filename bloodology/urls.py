from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('addRequest',views.AddRequestForm,name='addRequest'),
    path('allRepPost',views.all_posts,name='allRepPost'),
    path('signUp',views.user_signUp,name='signUp'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('profile',views.user_profile,name='profile'),
    path('All_Donors',views.all_Donors,name='All_Donors'),
    path('AboutBdonation',views.AboutBdonation,name='AboutBdonation'),
    path('deleteProfile/<int:id>/',views.deleteProfile, name="deleteProfile"),
    path('<int:id>/',views.updateProfile, name="updateProfile"),
    path('Blood_Donation_Tips',views.Blood_Donation_Tips, name="Blood_Donation_Tips"),
    path('advantage',views.advantageOfdonation, name="advantage"),
    path('Compatible',views.CompatibleBloodDonors, name="Compatible"),
    path('About',views.AboutUs, name="About"),
    path('password_reset/', views.request_password_reset, name='request_password_reset'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),


]
