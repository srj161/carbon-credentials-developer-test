import csv
import codecs
from datetime import datetime

from .. import models
from ..constants import UploadFileTypes


def upload(f, file_type):
    """
    Main entry point for the csv_uploader module.
    Parses the file and creates the corresponding entries in the database.
    There is some basic validation. If a row is invalid or there is a key clash, the
    row is skipped.

    Given more time, I would have implemented better validation and better user feedback
    of errors.

    args:
        f(file): csv file to upload
        file_type(int): an UploadFileType to denote the type of file
    """
    csv_file_dict = csv.DictReader(codecs.iterdecode(f, 'utf-8-sig'))
    csv_uploader = CSV_UPLOADERS[file_type]
    csv_uploader(csv_file_dict)


def _upload_building_data(rows):
    def _is_valid(row):
        return all([
            row.get('id') not in [None, ''],
            row.get('name') not in [None, ''],
            row.get('id', '').isdigit()
        ])

    models.Building.objects.bulk_create([
        models.Building(
            id=int(row['id']),
            name=row['name']
        ) for row in rows if _is_valid(row)
    ], ignore_conflicts=True)


def _upload_half_hourly_data(rows):
    def _is_valid(row):
        return all([
            row.get('consumption') not in [None, ''],
            row.get('meter_id') not in [None, ''],
            row.get('reading_date_time') not in [None, ''],
            row['meter_id'].isdigit()
        ])

    models.MeterReadings.objects.bulk_create([
        models.MeterReadings(
            consumption=float(row['consumption']),
            meter=models.Meter(id=row['meter_id']),
            reading_date_time=datetime.strptime(
                row['reading_date_time'], '%Y-%m-%d %H:%M')
        ) for row in rows if _is_valid(row)
    ], ignore_conflicts=True)


def _upload_meter_data(rows):
    def _is_valid(row):
        return all([
            row.get('building_id') not in [None, ''],
            row.get('id') not in [None, ''],
            row.get('fuel') not in [None, ''],
            row.get('unit') not in [None, ''],
        ])
    meters = []
    fuels = {f.name: f for f in models.Fuel.objects.all()}
    for row in rows:
        if not _is_valid(row):
            continue

        if row['fuel'] not in fuels.keys():
            fuel = models.Fuel.objects.create(
                name=row['fuel'],
                unit=row['unit']
            )
            fuels[row['fuel']] = fuel

        meters.append(
            models.Meter(
                id=row['id'],
                building=models.Building(id=row['building_id']),
                fuel=fuels[row['fuel']]
            )
        )
        models.Meter.objects.bulk_create(meters, ignore_conflicts=True)


CSV_UPLOADERS = {
    UploadFileTypes.BUILDING_DATA: _upload_building_data,
    UploadFileTypes.HALF_HOURLY_DATA: _upload_half_hourly_data,
    UploadFileTypes.METER_DATA: _upload_meter_data
}
