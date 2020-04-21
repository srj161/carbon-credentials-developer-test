from django.db import models


class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class Fuel(models.Model):
    UNIT_CHOICES = [
        ('m3', 'm3'),
        ('kWh', 'kWh')
    ]
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    name = models.CharField(max_length=50, unique=True)


class Meter(models.Model):
    id = models.IntegerField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)


class MeterReadings(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    consumption = models.DecimalField(decimal_places=5, max_digits=15)
    reading_date_time = models.DateTimeField(db_index=True)
