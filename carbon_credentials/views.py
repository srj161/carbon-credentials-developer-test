from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView

from .services import csv_uploader, chart_builder
from . import forms, models


@require_GET
def index(request):
    return render(request, 'carbon_credentials/index.html')


class UploadView(View):
    form = forms.UploadForm
    template = 'carbon_credentials/upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            csv_uploader.upload(
                request.FILES['upload_file'], form.cleaned_data['file_type'])

        return render(request, self.template, {'form': form})


class BuildingList(ListView):
    model = models.Building
    context_object_name = 'buildings'


class MeterList(ListView):
    model = models.Meter
    context_object_name = 'meters'

    def get_queryset(self):
        self.building = get_object_or_404(models.Building, pk=self.kwargs['building_id'])
        return models.Meter.objects.filter(building=self.building).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = self.building
        return context


class MeterReadingsList(ListView):
    model = models.MeterReadings
    context_object_name = 'meter_readings'

    def get_queryset(self):
        self.meter = get_object_or_404(models.Meter, pk=self.kwargs['meter_id'])
        return models.MeterReadings.objects.filter(meter=self.meter).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meter'] = self.meter
        return context


@require_GET
def visualise(request):
    if 'chart_type' not in request.GET:
        form = forms.VisualiseForm()
    else:
        form = forms.VisualiseForm(request.GET)

    chart = None
    if form.is_valid():
        meter = get_object_or_404(models.Meter, pk=form.cleaned_data['meter_id'])
        chart = chart_builder.build_chart(
            form.cleaned_data['chart_type'], meter)

    return render(request, 'carbon_credentials/visualise.html', {'form': form, 'chart': chart})
