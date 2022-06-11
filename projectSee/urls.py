
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [

    path('', views.landing, name='landing'),
    path('login/',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),

]
