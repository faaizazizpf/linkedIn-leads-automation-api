from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Campaign, CeleryJob, Label
from celery.task.control import revoke


@receiver(post_save, sender=Campaign)
def stop_campaign(sender, instance, created, *args, **kwargs):

    lead, created = Label.objects.get_or_create(user = instance.user, name = "Lead")
    customer, created = Label.objects.get_or_create(user = instance.user, name = "Customer")
    
    if instance.status == "Stopped":
        print("Stopping Campaign")
        for job in CeleryJob.objects.filter(campaign=instance):
            print(job)
            revoke(job.task_id, terminate=True)