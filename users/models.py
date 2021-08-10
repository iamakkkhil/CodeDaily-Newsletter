from django.db import models
import uuid

# Create your models here.
class Profile(models.Model):
    email = models.EmailField(max_length=500)
    verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.email)


class DayTrack(models.Model):
    profileOwner = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    currentDay = models.IntegerField(default=1, null=True, blank=True)
    paused = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.profileOwner.email) +" : " +str(self.currentDay)