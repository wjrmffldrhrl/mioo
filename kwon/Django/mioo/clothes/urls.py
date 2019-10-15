from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('crawling', views.crawling),

]
