from django.test import TestCase
from django.test.client import Client
from mainapp.models import ArtObject, ArtCategory
from django.core.management import call_command
from django.urls import reverse
from mainapp.views import product

class TestMainappSmoke(TestCase):
    
    fixtures = ['mainapp.json']
    
    def setUp(self):
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get(reverse('mainapp:index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('mainapp:contacts'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('mainapp:catalog'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/products/2/')
        self.assertEqual(response.status_code, 200)

        for product in ArtObject.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',
    #                  'basketapp')
