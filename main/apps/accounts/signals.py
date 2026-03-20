from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == "freelancer":
        from .models import FreelancerProfile
        FreelancerProfile.objects.get_or_create(user=instance)

    elif instance.role == "client":
        from .models import ClientProfile
        ClientProfile.objects.get_or_create(user=instance)