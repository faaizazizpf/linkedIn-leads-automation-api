from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserProfile, LinkedinAccount
from main.api.tasks import check_user_connections


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=LinkedinAccount)
def crawl_user_connections(sender, instance, created, *args, **kwargs):

    if instance.connected and instance.ready_for_use:
        check_user_connections.delay(instance.profile.user.id, {"connected" : True, "ready_for_use" : True, "id": f"{instance.id}"})