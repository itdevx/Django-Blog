from django.urls import path
from .views import IndexView, DetailBlogView, ListBlogView

app_name = 'blog'


urlpatterns = [
    path(
        '', IndexView.as_view(), name='index'
    ),
    path(
        'detail', DetailBlogView.as_view(), name='detail'
    ),
    path(
        'list', ListBlogView.as_view(), name='list'
    )
]
