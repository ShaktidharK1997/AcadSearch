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

class Author(models.Model):
    author_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Journal(models.Model):
    journal_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    pages = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Paper(models.Model):
    corpus_id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    citation_count = models.IntegerField(null=True, blank=True)
    influential_citation_count = models.IntegerField(null=True, blank=True)
    is_open_access = models.BooleanField(default=False)
    url = models.URLField(max_length=500)
    publication_date = models.DateField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
