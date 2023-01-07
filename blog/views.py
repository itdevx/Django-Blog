from django.http import request
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Category, Article
from django.db.models import Count


class IndexView(View):
    template_name = 'blog-templates/index-magazine.html'

    def get(self, request):
        article_ = Article.objects.filter(status=1)
        context = {
            'article_': article_
        }
        return render(request, self.template_name, context)


class DetailBlogView(View):
    template_name = 'blog-templates/magazine-news-detail.html'

    def get(self, request, pk, slug):
        article = get_object_or_404(Article, id=pk, slug=slug, status=1)
        last_article = Article.objects.filter(status=1)[:3]
        article_ = Article.objects.filter(status=1)

        context = {
            'article': article,
            'la': last_article,
            'article_': article_,
        }

        return render(request, self.template_name, context)


class ListBlogView(View):
    template_name = 'blog-templates/list-magazine.html'

    def get(self, request):
        return render(request, self.template_name)


class SearchFieldView(ListView):
    template_name = 'blog-templates/list-magazine.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all().annotate(articles_count=Count('article'))
        context['article_'] = Article.objects.filter(status=1)
        return context


    def get_queryset(self):
        q = self.request.GET.get('q')
        if q is not None:
            return Article.objects.search(q)
        return Article.objects.filter(status=1)


