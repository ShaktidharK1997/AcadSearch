from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username