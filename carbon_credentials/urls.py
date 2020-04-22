from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('explore/', views.BuildingList.as_view(), name='explore'),
    path('explore/building/<int:building_id>', views.MeterList.as_view(), name='explore_building'),
    path('explore/meter/<int:meter_id>', views.MeterReadingsList.as_view(), name='explore_meter'),
    path('visualise/', views.visualise, name='visualise'),
    path('admin/', admin.site.urls)
]
