from django.urls import reverse
from django.test import TestCase

from .. import models


class TestIndex(TestCase):
    def test_index_renders_correct_html(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carbon_credentials/index.html')
        # Checks links are visible in response
        self.assertContains(response, '<a href="/upload/">Upload Data</a>')
        self.assertContains(response, '<a href="/explore/">Explore Data</a>')
        self.assertContains(response, '<a href="/visualise/">Visualise Data</a>')

    def test_index_raises_405_with_a_POST_request(self):
        response = self.client.post(reverse('index'))
        self.assertEqual(response.status_code, 405)


class TestExplore(TestCase):
    def test_renders_with_correct_queryset_when_no_buildings(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['buildings'], [])

    def test_buildings_are_returned_in_response(self):
        # Create some buildings
        models.Building.objects.bulk_create([
            models.Building(id=1, name='Building 1'),
            models.Building(id=2, name='Building 2')
        ])
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carbon_credentials/building_list.html')
        self.assertQuerysetEqual(
            list(response.context['buildings']), [
                '<Building: Building object (1)>',
                '<Building: Building object (2)>'
            ]
        )

    def test_links_and_name_are_correctly_formatted_in_response(self):
        models.Building.objects.create(id=1, name='Building 1')
        response = self.client.get(reverse('explore'))
        self.assertContains(response, '<td><a href="/explore/building/1">1</a></td>')
        self.assertContains(response, '<td>Building 1</td>')

    def test_raises_2342_with_a_POST_request(self):
        response = self.client.post(reverse('explore'))
        self.assertEqual(response.status_code, 405)


class TestUpload(TestCase):
    def test_renders_form_correctly_in_a_GET_request(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carbon_credentials/upload.html')
        # File in form
        self.assertContains(
            response,
            '<input type="file" name="upload_file" required id="id_upload_file">'
        )
        # File type in form
        self.assertContains(
            response,
            '<select name="file_type" id="id_file_type">'
        )
        # submit button
        self.assertContains(
            response,
            '<input type="submit"'
        )
