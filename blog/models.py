from django.db import models
from account.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
import readtime
from django.db.models import Q
from extentions.utils import jalali_converter
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Manager(models.Manager):
    def search(self, q):
        get_article = Q(title__icontains=q) | Q(description__icontains=q)
        return self.get_queryset().filter(get_article, status=1).distinct()

    def categories(self, slug):
        return self.get_queryset().filter(category__category_slug__iexact=slug, status=1).distinct()
        

class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name=' دسته بندی را وارد کنید')
    category_slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.category_name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


STATUS = (
    ('1', 'منتشر شده'),
    ('2', 'منتشر نشده')
)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(null=True, blank=True, unique=True, allow_unicode=True, max_length=255)
    date = models.DateField(auto_now=True, verbose_name='تاریخ')
    status = models.CharField(choices=STATUS, max_length=1, verbose_name='وضعیت')
    image = models.ImageField(upload_to='article-image-intro', verbose_name='تصویر')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    description = RichTextField(verbose_name='مقاله')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته بندی')
    objects = Manager()
    hit_count_generic = GenericRelation(HitCount, object_id_field='pk', related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('blog:detail-article', args=[self.pk, self.slug])

    @property
    def get_readtime(self):
        result = readtime.of_text(self.description)
        res = str(result.text)
        return res.replace('min', 'دقیقه')
    
    @property
    def get_date(self):
        return jalali_converter(self.date)

    @property
    def get_absolut_author(self):
        return reverse('blog:author-view', args=[self.author.username])
    
    @property
    def get_url_for_delete(self):
        return reverse('account:delete-article', args=[self.id, self.slug])
