from django.urls import path, include

from . import views 

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', views.search_articles, name='search_articles'),
    path('search/', views.search_articles, name='search_articles'),
    path('paper/', views.get_paper_info, name= 'search_paper'),
]