
# from msilib.schema import ListView
from django.views.generic import ListView
from django.urls import path
from django.urls import include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('', views.landing, name='landing'),
    path('login/',views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('welcome', views.welcome, name='welcome'),
    # path('welcome', views.welcome, name='welcome'),
    path('like/<str:pk>',views.likeProject,name='like_project'),
    path('profile/<str:username>', views.PostListView.as_view(),name='profile'),
    path('profile/<str:username>', views.ProfileListView.as_view(),name='profile1'),
    # path('profile/<str:username>', views.ProfiletListView.as_view(),name='user-profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('new_post', views.new_post, name='new_post'),
    path('ajax/newsletter/', views.newsletter, name='newsletter'),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/projects/', views.ProjectsList.as_view()),  


]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

