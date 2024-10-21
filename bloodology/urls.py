from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name='home'),
    path('addRequest',views.AddRequestForm,name='addRequest'),
    path('updateaddRequest/<int:post_id>/', views.edit_blood_request, name='updateaddRequest'),
    path('allRepPost',views.all_posts,name='allRepPost'),
    path('signUp',views.user_signUp,name='signUp'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('profile',views.user_profile,name='profile'),
    path('All_Donors',views.all_Donors,name='All_Donors'),
    path('AboutBdonation',views.AboutBdonation,name='AboutBdonation'),
    path('updateProfile/<int:id>/', views.updateProfile, name="updateProfile"),
    path('deleteProfile/<int:id>/', views.deleteProfile, name="deleteProfile"),
    path('Blood_Donation_Tips',views.Blood_Donation_Tips, name="Blood_Donation_Tips"),
    path('advantage',views.advantageOfdonation, name="advantage"),
    path('Compatible',views.CompatibleBloodDonors, name="Compatible"),
    path('About',views.AboutUs, name="About"),
    path('password_reset/', views.request_password_reset, name='request_password_reset'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('blogapost', views.blog_post, name='blogapost'),
    path('blogapostform', views.blogPostFormview, name='blogapostform'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashbloodReq', views.dash_blood_requests, name='dashbloodReq'),
    path('updateBlogPost/<int:id>/', views.edit_blog_post, name="updateBlogPost"),
    path('deleteBlogPost/<int:id>/', views.delete_blog_post, name="deleteBlogPost"),


]
