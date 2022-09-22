from django.test import TestCase, Client
from django.urls import resolve

class MyWatchListViewsTest(TestCase):
    def test_html_view(self):
        response = self.client.get('/mywatchlist/html', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_xml_view(self):
        response = self.client.get('/mywatchlist/xml', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_json_view(self):
        response = self.client.get('/mywatchlist/json', follow=True)
        self.assertEqual(response.status_code, 200)