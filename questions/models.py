from django.db import models
import uuid
from froala_editor.fields import FroalaField

# Create your models here.
class Question(models.Model):
    LEVEL = (
        ('Beginner', 'Level 0'),
        ('Medium', 'Level 1'),
        ('Hard', 'Level 2'),
        ('Expert', 'Level 3')
    )

    title = models.CharField(max_length=500, null=True, blank=True)
    tag = models.CharField(max_length=500, null=True, blank=True)
    dayNo = models.IntegerField(unique=True, null=True, blank=True)
    difficulty = models.CharField(default='Level 0', max_length=20, choices=LEVEL)
    company = models.CharField(max_length=500, null=True, blank=True)
    report = models.IntegerField(default=0, null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)
    code =  FroalaField()
    time_cmplx = models.CharField(max_length=100, null=True, blank=True)
    space_cmplx = models.CharField(max_length=100, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return "Day_"+str(self.dayNo) +": "+str(self.title)
