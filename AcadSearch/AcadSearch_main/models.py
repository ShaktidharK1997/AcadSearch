from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save()