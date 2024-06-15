from django.urls import path, include

from . import views 

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', views.search_articles, name='search_articles'),
    path('search/', views.search_articles, name='search_articles'),
    path('paper/', views.get_paper_info, name= 'search_paper'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('api/online-users/', views.get_online_users, name='online_users'),
]