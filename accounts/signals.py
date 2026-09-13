from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Profile when a User is saved.
    """
    profile, created = Profile.objects.get_or_create(user=instance)
    if created:
        print('Profile created!')
    else:
        profile.save()
        print('Profile updated!')