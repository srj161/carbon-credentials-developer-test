from jchart import Chart

from .. import models


class LineChart(Chart):
    chart_type = 'line'

    def get_datasets(self, **kwargs):
        meter = models.Meter.objects.get(pk=8754)
        readings = models.MeterReadings.objects.filter(meter=meter)
        return [{
            'label': "My Dataset",
            'data': [reading.consumption for reading in readings]
        }]

    def get_labels(self, **kwargs):
        meter = models.Meter.objects.get(pk=8754)
        readings = models.MeterReadings.objects.filter(meter=meter)
        return [reading.reading_date_time for reading in readings]

