from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_delete, sender=UserProfile)
def delete_user_with_profile(sender, instance, **kwargs):
    # Delete the related User instance when the UserProfile is deleted
    user = instance.user
    if user:
        user.delete()
