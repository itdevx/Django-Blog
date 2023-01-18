from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Category, Article
from django.db.models import Count
from extentions.utils import jalali_converter
import datetime
from random import randint
from account.models import User


class IndexView(View):
    template_name = 'blog-templates/index-magazine.html'

    def get(self, request):
        article_ = Article.objects.filter(status=1)
        first_articles = Article.objects.filter(status=1).order_by('-id')[:4]
        first_articles_big = Article.objects.filter(status=1).order_by('-id')[4:5]
        last_article = Article.objects.filter(status=1).order_by('-id')[:6]
        if article_:
            random_ = randint(1, len(article_))
            random_article = Article.objects.filter(status=1)[int(random_)-1]
        else:
            random_article = Article.objects.filter(status=1)[0:1]
        # after -> change number
        bilow_random_article = Article.objects.filter(status=1)[:4]

        context = {
            'article_': article_,
            'category': Category.objects.all().annotate(articles_count=Count('article')),
            'f_a': first_articles,
            'f_a_b': first_articles_big,
            'date': jalali_converter(datetime.datetime.now()),
            'l_a': last_article,
            'r_a': random_article,
            'b_a': bilow_random_article
        }
        return render(request, self.template_name, context)


class DetailBlogView(View):
    template_name = 'blog-templates/magazine-news-detail.html'

    def get(self, request, pk, slug):
        article = get_object_or_404(Article, id=pk, slug=slug, status=1)
        last_article = Article.objects.filter(status=1).order_by('-id')[:3]
        article_ = Article.objects.filter(status=1)
        related_article = Article.objects.filter(category__article=article, status=1).distinct()[:2]

        context = {
            'article': article,
            'la': last_article,
            'article_': article_,
            'category': Category.objects.all(),
            'r_a': related_article,
            'date': jalali_converter(datetime.datetime.now())
        }
        return render(request, self.template_name, context)


class SearchFieldView(ListView):
    template_name = 'blog-templates/list-magazine.html'
    context_object_name = 'article'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all().annotate(articles_count=Count('article'))
        context['article_'] = Article.objects.filter(status=1)
        context['last_article'] = Article.objects.filter(status=1).order_by('-id')[:3]
        context['date'] = jalali_converter(datetime.datetime.now())
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q is not None:
            return Article.objects.search(q)
        return Article.objects.filter(status=1)


class CategoryView(ListView):
    template_name = 'blog-templates/list-magazine.html'
    context_object_name = 'article'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all().annotate(articles_count=Count('article'))
        context['article_'] = Article.objects.filter(status=1)
        context['last_article'] = Article.objects.filter(status=1).order_by('-id')[:3]
        context['date'] = jalali_converter(datetime.datetime.now())

        return context

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.filter(category_name__iexact=slug).first()
        if category is None:
            return Article.objects.categories(slug)
        else:
            return
    

class AuthorView(ListView):
    template_name = 'blog-templates/author.html'
    context_object_name = 'article'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all().annotate(articles_count=Count('article'))
        context['article_'] = Article.objects.filter(status=1)
        context['last_article'] = Article.objects.filter(status=1).order_by('-id')[:3]
        context['date'] = jalali_converter(datetime.datetime.now()),
        context['author'] = User.objects.get(username=self.kwargs['username'])
        return context

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(author__username=self.kwargs['username']).all()
        
        