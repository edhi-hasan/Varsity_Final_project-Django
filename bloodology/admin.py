from django.contrib import admin
from . models import *

# Register your models here.
@admin.register(BloodRequestPost)
class postmodeladmin(admin.ModelAdmin):
    list_display=['id','blood_group','date_time','Disease_name','No_of_bag','medical_name','location','phone_number','created_at']

# Admin for UserProfile with ID included in list_display
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'blood_group', 'phone_number', 'address']
