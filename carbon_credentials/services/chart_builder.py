from django.db.models import Count

from jchart import Chart
from jchart.config import Axes, Legend, rgba, ScaleLabel, Title

from .. import models
from ..constants import ChartTypes


def build_chart(chart_type, meter):
    if chart_type == ChartTypes.METER_TIME:
        return MeterTimeChart(meter)
    if chart_type == ChartTypes.METER_INSTALLATION:
        return MeterInstallationChart()


class MeterTimeChart(Chart):
    chart_type = 'line'
    legend = Legend(display=False)
    title = Title(display=True, text='Meter Consumption Over Time')

    def __init__(self, meter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readings = models.MeterReadings.objects.filter(meter=meter)
        self.scales = {
            'yAxes': [
                Axes(scaleLabel=ScaleLabel(
                    display=True,
                    labelString=f'{meter.fuel.name} ({meter.fuel.unit})'
                ))
            ]
        }

    def get_datasets(self, **kwargs):
        return [{
            'label': 'Meter Consumption over time',
            'data': [reading.consumption for reading in self.readings]
        }]

    def get_labels(self, **kwargs):
        return [
            reading.reading_date_time.strftime("%m/%d/%Y %H:%M")
            for reading in self.readings
        ]


class MeterInstallationChart(Chart):
    chart_type = 'doughnut'
    title = Title(display=True, text='Meter Installation by Fuel Type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meters_qs = models.Meter.objects.values('fuel__name').annotate(Count('fuel'))

    def get_datasets(self, **kwargs):
        return [{
            'data': [m['fuel__count'] for m in self.meters_qs],
            'backgroundColor': [
                rgba(225, 0, 0),
                rgba(0, 225, 0),
                rgba(0, 0, 225)
            ]
        }]

    def get_labels(self, **kwargs):
        return [m['fuel__name'] for m in self.meters_qs]
