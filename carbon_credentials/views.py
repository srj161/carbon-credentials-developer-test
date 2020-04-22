from django.shortcuts import get_object_or_404, render
from django.views import View

from . import csv_uploader, forms, models


def index(request):
    return render(request, 'index.html')


class UploadView(View):
    form = forms.UploadForm
    template = 'upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            csv_uploader.upload(
                request.FILES['upload_file'], form.cleaned_data['file_type'])

        return render(request, self.template, {'form': form})


def explore(request):
    context = {
        'buildings': models.Building.objects.all().order_by('id')
    }
    return render(request, 'explore.html', context)


def explore_building(request, building_id):
    building = get_object_or_404(models.Building, pk=building_id)
    meters = models.Meter.objects.filter(building=building).order_by('id')
    context = {
        'building': building,
        'meters': meters
    }
    return render(request, 'explore_building.html', context)


def explore_meter(request, meter_id):
    meter = get_object_or_404(models.Meter, pk=meter_id)
    readings = models.MeterReadings.objects.filter(meter=meter).order_by('reading_date_time')
    context = {
        'meter': meter,
        'readings': readings
    }
    return render(request, 'explore_meter.html', context)


def visualise(request):
    pass
