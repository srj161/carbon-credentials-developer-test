from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('explore/', views.explore, name='explore'),
    path('visualise/', views.visualise, name='visualise'),
    path('admin/', admin.site.urls),
]
