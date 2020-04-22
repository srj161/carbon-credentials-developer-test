from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic.list import ListView

from .services import csv_uploader, chart_builder
from . import forms, models


@require_GET
def index(request):
    """ Basic entry page for the site """
    return render(request, 'carbon_credentials/index.html')


class UploadView(View):
    """ View to upload data from csvs. Accepts GET and POST requests. """
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
    """ View for the list of all Buildings """
    model = models.Building
    context_object_name = 'buildings'


class MeterList(ListView):
    """
    View for the list of meters for a given building.
    Returns 404 if the Building cannot be found.
    """
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
    """
    View the list of meter readings for a given meter.
    Returns 404 if the Meter cannot be found.
    """
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
    """
    Visualisation view renders a page from the VisualiseForm.
    If the form contains a chart_type, the view renders the chart.
    Only accepts GET request.
    """
    if 'chart_type' not in request.GET:
        # If there is no chart_type, we can assume this request has not been posted by the form
        # so don't pass in any GET data.
        form = forms.VisualiseForm()
    else:
        form = forms.VisualiseForm(request.GET)

    chart = None
    if form.is_valid():
        meter = get_object_or_404(models.Meter, pk=form.cleaned_data['meter_id'])
        chart = chart_builder.build_chart(
            form.cleaned_data['chart_type'], meter)

    return render(request, 'carbon_credentials/visualise.html', {'form': form, 'chart': chart})
