from django.db.models import Count, Sum
from django.db.models.functions import Trunc

from jchart import Chart
from jchart.config import Axes, Legend, rgba, ScaleLabel, Title

from .. import models
from ..constants import ChartTypes


def build_chart(chart_type, meter):
    """
    Main entry point for the chart_builder module.

    args:
        chart_type(int): a ChartType representing the desired chart.
        meter(Meter): a meter model used in the generation of charts.

    returns:
        Chart: an object of a subclass of Chart for this chart_type
    """
    if chart_type == ChartTypes.METER_TIME:
        return MeterTimeChart(meter)
    if chart_type == ChartTypes.METER_INSTALLATION:
        return MeterInstallationChart()
    if chart_type == ChartTypes.METER_TIME_DAY_AGG:
        return MeterDailyBreakdowChart(meter)


class MeterTimeChart(Chart):
    """
    A line type chart that displays the meter consumption over time for a
    given meter.
    """
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
            reading.reading_date_time.strftime("%d/%m/%Y %H:%M")
            for reading in self.readings
        ]


class MeterDailyBreakdowChart(Chart):
    """
    A Bar chart to display the monthly meter usage
    """
    chart_type = 'bar'
    legend = Legend(display=False)
    title = Title(display=True, text='Meter Consumption per month')

    def __init__(self, meter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readings = models.MeterReadings.objects.filter(meter=meter) \
            .annotate(reading_day=Trunc('reading_date_time', 'day')) \
            .values('reading_day') \
            .annotate(consumption=Sum('consumption'))
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
            'data': [reading['consumption'] for reading in self.readings]
        }]

    def get_labels(self, **kwargs):
        return [
            reading['reading_day'].strftime("%d/%m/%Y")
            for reading in self.readings
        ]


class MeterInstallationChart(Chart):
    """
    A doughnut chart that displays the number of each type of meter we have data
    for.
    """
    chart_type = 'doughnut'
    title = Title(display=True, text='Meter Installation by Fuel Type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Creates a queryset returning 'fuel__count' and 'fuel__name' fields
        self.meters_qs = models.Meter.objects.values('fuel__name').annotate(Count('fuel'))

    def get_datasets(self, **kwargs):
        return [{
            'data': [m['fuel__count'] for m in self.meters_qs],
            # Colors the segments of the chart
            'backgroundColor': [
                rgba(225, 0, 0),
                rgba(0, 225, 0),
                rgba(0, 0, 225)
            ]
        }]

    def get_labels(self, **kwargs):
        return [m['fuel__name'] for m in self.meters_qs]
