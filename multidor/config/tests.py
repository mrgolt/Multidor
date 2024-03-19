from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Content

class ContentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_content')

    def test_create_content(self):
        data = {
            "site": 2,
            "text": "Some text",
            "category": "Some category",
            "title": "Some title",
            "description": "Some description",
            "keywords": "Some keywords",
            "slug": "slug",
            "is_main": False
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(Content.objects.get().title, 'Some title')

