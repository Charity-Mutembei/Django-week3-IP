
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [

    path('', views.landing, name='landing'),
    path('login/',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('welcome', views.welcome, name='welcome'),
    path('ajax/newsletter/', views.newsletter, name='newsletter'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/projects/', views.ProjectsList.as_view()),  


]
