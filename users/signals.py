from django.db.models.signals import post_save, post_delete
from .models import DayTrack, Profile


def createDayTrack(sender, instance, created, **kwargs):
    if created:
        profileOwner=instance
        DayTrackObj = DayTrack.objects.create(
            profileOwner=profileOwner, 
        )

def deleteProfile(sender, instance, **kwargs):
    user=instance.profileOwner
    user.delete()
    

# another way of connecting signals to models
post_save.connect(createDayTrack, sender=Profile)
post_delete.connect(deleteProfile, sender=DayTrack)