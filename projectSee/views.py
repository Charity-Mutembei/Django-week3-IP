# from msilib.schema import ListView
from django.views.generic import ListView
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import registrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewsLetterForm, PostMakeForm, ProfileEditForm
from .models import NewsLetterRecipients
from .email import send_welcome_email
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView,status
from .models import Projects, Profile
from .serializer import ProfileSerializer, ProjectsSerializer
from projectSee import serializer
from .permissions import IsAdminOrReadOnly
from django.urls import reverse


# Create your views here.
def registerPage(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)

            messages.success(request,('Registration successfull'))

            return redirect('landing')

    else:
        form=registrationForm()
    return render(request, 'register.html', {'form': form})   

def loginPage(request):

    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')

        else:
            messages.success(request, ('There was an error! Please try again'))
            return redirect('login')

    else:
        return render(request, 'login.html')

@login_required(login_url='/login/')
def landing(request):
    return render(request, 'landing.html') 

def welcome(request):
    projects = Projects.objects.all() 
    user = request.user
    profiles = Profile.objects.filter(user=user.id)

          
   
    return render (request, 'welcome.html', {'projects': projects, 'profiles': profiles})

class ProfiletListView(ListView):
    model = Profile
    template_name = 'welcome.html'
    context_object_name = 'profiles'


    def get_query_set(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.filter(author = user)

def newsletter(request):
    name = request.POST.get('your name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name,email)
    data = {'success': 'You have been successfully added to the mailing list'}
    return JsonResponse


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        permission_classes = (IsAdminOrReadOnly,)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsList(APIView):
    def get(self, request, format=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects, many=True)
        permission_classes = (IsAdminOrReadOnly,)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def new_post(request):
    current_user = request.user
    form = PostMakeForm()
    
    if request.method == 'POST':
        form = PostMakeForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.editor = current_user
            post.save()
        return redirect('welcome')
    else:
        form = PostMakeForm()
    return render(request, 'new_post.html', {'form': form})

@login_required(login_url='/login/')
class profileListView(ListView):
    def profile (self, request):
        profile = request.user.profile
        user= self.request.user.profile
        projects = Projects.objects.filter(author=user)


        return render (request,'profile.html', {'projects': projects, 'profile': profile})

@login_required(login_url='/log/')
def edit_profile(request):
    current_user = request.user
    form = ProfileEditForm()
    username = current_user.username

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.editor = current_user
            profile.save()

        return redirect('profile', username=username )

    else:
        form = ProfileEditForm()
    return render(request, 'edit.html', {'form':form})

class PostListView(ListView):
    model = Projects
    template_name = 'profile.html'
    context_object_name = 'projects'


    def get_query_set(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Projects.objects.filter(author = user).order_by('-date_posted')

class ProfileListView(ListView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'


    def get_query_set(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.filter(author = user).order_by('-date_posted')

@login_required(login_url='/login/')
def likeProject(request, pk):
    project = get_object_or_404(Projects, id=request.POST.get('like_id'))
    project.likes.add(request.user)
    return HttpResponseRedirect(reverse('welcome', ))
