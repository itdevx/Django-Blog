from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import SearchFieldView, IndexView, DetailBlogView


class TestUrls(SimpleTestCase):
    pass
    # def test_search_url_is_resolved(self):
    #     url = reverse('blog:search')
    #     self.assertEqual(resolve(url), SearchFieldView.as_view())

    # def test_index_url_is_resolved(self):
    #     url = reverse('blog:index')
    #     self.assertEqual(resolve(url), IndexView.as_view())

    # def test_detail_url_is_resolved(self):
    #     url = reverse('blog:detail-article', args=['this-is-test'])
    #     self.assertEqual(resolve(url), DetailBlogView.as_view())