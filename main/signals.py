from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def add_user_to_farmer_group(sender, instance, created, **kwargs):
    if created:
        # Check if the 'farmer' group exists
        group, created = Group.objects.get_or_create(name='farmer')
        # Add the user to the 'farmer' group
        instance.groups.add(group)
