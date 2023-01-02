from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.category_name


STATUS = (
    ('1', 'منتشر شده'),
    ('2', 'منتشر نشده')
)


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=1)
    image = models.ImageField(upload_to='article-image-intro')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
