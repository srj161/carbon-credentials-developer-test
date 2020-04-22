from django.test import TestCase

from io import BytesIO

from ..services import csv_uploader
from .. import constants, models


class TestUploadBuildingData(TestCase):
    def test_correctly_reads_csv_file_and_creates_buildings(self):
        csv_file = BytesIO(b'id,name\n1,Building 1\n2,Building 2')
        csv_uploader.upload(csv_file, constants.UploadFileTypes.BUILDING_DATA)
        buildings = models.Building.objects.all()

        building_1 = buildings[0]
        self.assertEqual(building_1.id, 1)
        self.assertEqual(building_1.name, 'Building 1')

        building_2 = buildings[1]
        self.assertEqual(building_2.id, 2)
        self.assertEqual(building_2.name, 'Building 2')

    def test_ignores_empty_lines_in_csv(self):
        csv_file = BytesIO(b'id,name\n1,Building 1\n,')
        csv_uploader.upload(csv_file, constants.UploadFileTypes.BUILDING_DATA)
        buildings = models.Building.objects.all()
        self.assertEqual(len(buildings), 1)

    def test_ignores_where_id_is_invalid_in_csv(self):
        csv_file = BytesIO(b'id,name\n1,Building 1\nhello,Building 2')
        csv_uploader.upload(csv_file, constants.UploadFileTypes.BUILDING_DATA)
        buildings = models.Building.objects.all()
        self.assertEqual(len(buildings), 1)

    def test_doesnt_fail_on_primary_key_violation(self):
        # Duplicate primary means only on building is created
        csv_file = BytesIO(b'id,name\n1,Building 1\n1,Building 2')
        csv_uploader.upload(csv_file, constants.UploadFileTypes.BUILDING_DATA)
        buildings = models.Building.objects.all()
        self.assertEqual(len(buildings), 1)
