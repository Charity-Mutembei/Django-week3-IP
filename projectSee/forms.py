from dataclasses import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import Profile, Projects



class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class NewsLetterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class PostMakeForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'image', 'description', 'link']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'picture', 'Bio', 'contacts']