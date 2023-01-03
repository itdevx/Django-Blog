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
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, verbose_name='آدرس')
    date = models.DateField(auto_now=True, verbose_name='تاریخ')
    status = models.CharField(choices=STATUS, max_length=1, verbose_name='وضعیت')
    image = models.ImageField(upload_to='article-image-intro', verbose_name='تصویر')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    description = RichTextField(verbose_name='مقاله')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی')

    def __str__(self):
        return self.title
