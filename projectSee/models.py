from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()


class Profile(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(null=True, upload_to = 'profiles')
    Bio = models.TextField(max_length=500, null=False)
    contacts = models.TextField(max_length=100, null=False, default='')



    def __str__(self):
        return str(self.user)


    def save_profile(self):
        self.save()


class Projects(models.Model):
    title = models.CharField(max_length=50, null=False)
    image = models.ImageField(null=True, upload_to='projects')
    description = models.TextField(max_length=300)
    link = models.CharField(max_length=150)


    def __str__(self):
        return str(self.user)

    def save_projects(self):
        self.save()