from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import registrationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import NewsLetterForm
from .models import NewsLetterRecipients
from .email import send_welcome_email


# Create your views here.
def registerPage(request):
    form = registrationForm()
    if request.method == 'POST':
        form = registrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = form.save()
            login(request,user,backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect ('landing')

    return render(request, 'register.html', {'form':form})    

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('landing')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('landing')

        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    context = {}

    return render(request, 'login.html', context)

@login_required(login_url='/login/')
def landing(request):
    return render(request, 'landing.html') 

def welcome(request):
    form = NewsLetterForm()
   
    return render (request, 'welcome.html', {'form': form})

def newsletter(request):
    name = request.POST.get('your name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name,email)
    data = {'success': 'You have been successfully added to the mailing list'}
    return JsonResponse
