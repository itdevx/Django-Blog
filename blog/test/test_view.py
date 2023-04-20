from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Article, Category
import json


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.search_url = reverse('blog:search')

    def test_project_search_GET(self):
        client = Client()
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog-templates/list-magazine.html')