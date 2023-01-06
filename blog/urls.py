from django.urls import path
from .views import IndexView, DetailBlogView, ListBlogView

app_name = 'blog'


urlpatterns = [
    path(
        '', IndexView.as_view(), name='index'
    ),
    path(
        'article/<int:pk>/<slug:slug>', DetailBlogView.as_view(), name='detail-article'
    ),
    path(
        'list', ListBlogView.as_view(), name='list'
    )
]
