from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BloodRequestPost(models.Model):
        BLOOD_GROUP_CHOICES = [
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
        ]

        blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES)
        date_time = models.DateTimeField()
        Disease_name = models.CharField(max_length=100)
        No_of_bag = models.IntegerField()
        medical_name = models.CharField( max_length=150)
        location = models.CharField(max_length=255)
        phone_number = models.CharField(max_length=15)
        created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        name = models.CharField(max_length=150)
        blood_group = models.CharField(max_length=5)
        phone_number = models.CharField(max_length=15)
        address = models.CharField(max_length=250)
        profile_img = models.ImageField(upload_to='Images')

        def __str__(self):
                return self.name
