from django.test import TestCase

from .. import forms, models
from ..constants import ChartTypes


class TestVisualiseForm(TestCase):
    def test_form_is_valid_with_valid_data(self):
        form = forms.VisualiseForm(data={
            'chart_type': ChartTypes.METER_TIME,
            'meter_id': 2
        })
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_missing_meter_id(self):
        form = forms.VisualiseForm(data={
            'chart_type': ChartTypes.METER_TIME
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'meter_id': ['Please enter a meter id']})

    def test_form_is_not_valid_missing_chart_type(self):
        form = forms.VisualiseForm(data={
            'meter_id': 2
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'chart_type': ['This field is required.']})

    def test_form_is_initialised_with_correct_fields(self):
        form = forms.VisualiseForm()
        self.assertIn('chart_type', form.fields)
        self.assertIn('meter_id', form.fields)

    def test_form_widget_id_field_choices_are_populated_correctly(self):
        fuel = models.Fuel.objects.create(unit='m3', name='Natural Gas')
        building = models.Building.objects.create(id=1, name='Building 1')
        models.Meter.objects.create(id=1, building=building, fuel=fuel)
        models.Meter.objects.create(id=2, building=building, fuel=fuel)

        form = forms.VisualiseForm()
        self.assertEqual(form.fields['meter_id'].widget.choices, [(1, '1'), (2, '2')])
