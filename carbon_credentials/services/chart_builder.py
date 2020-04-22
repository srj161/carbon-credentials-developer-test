from jchart import Chart
from jchart.config import Axes, Legend, ScaleLabel, Title

from .. import models
from ..constants import ChartTypes


def build_chart(chart_type, meter):
    if chart_type == ChartTypes.METER_TIME:
        return MeterTimeChart(meter)


class MeterTimeChart(Chart):
    chart_type = 'line'
    legend = Legend(display=False)
    title = Title(display=True, text='Meter Consumption Over Time')

    def __init__(self, meter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meter = meter
        self.scales = {
            'yAxes': [
                Axes(scaleLabel=ScaleLabel(
                    display=True,
                    labelString=f'{meter.fuel.name} ({meter.fuel.unit})'
                ))
            ]
        }

    def get_datasets(self, **kwargs):
        readings = models.MeterReadings.objects.filter(meter=self.meter)
        return [{
            'label': 'Meter Consumption over time',
            'data': [reading.consumption for reading in readings]
        }]

    def get_labels(self, **kwargs):
        meter = models.Meter.objects.get(pk=8754)
        readings = models.MeterReadings.objects.filter(meter=meter)
        return [
            reading.reading_date_time.strftime("%m/%d/%Y %H:%M")
            for reading in readings
        ]
