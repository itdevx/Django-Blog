from django.urls import path
from .views import IndexView, DetailBlogView, ListBlogView, SearchFieldView, CategoryView

app_name = 'blog'


urlpatterns = [
    path(
        '', IndexView.as_view(), name='index'
    ),
    path(
        'article/<int:pk>/<slug:slug>/', DetailBlogView.as_view(), name='detail-article'
    ),
    path(
        'article/<slug>/', CategoryView.as_view(), name='category'
    ),
    path(
        'search/', SearchFieldView.as_view(), name='search'
    ),
]
