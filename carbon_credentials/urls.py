from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('explore/', views.explore, name='explore'),
    path('explore/building/<int:building_id>', views.explore_building, name='explore_building'),
    path('explore/meter/<int:meter_id>', views.explore_meter, name='explore_meter'),
    path('visualise/', views.visualise, name='visualise'),
    path('admin/', admin.site.urls),
]
