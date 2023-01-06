from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, DetailView
from .models import Category, Article


class IndexView(View):
    template_name = 'blog-templates/index-magazine.html'

    def get(self, request):
        return render(request, self.template_name)


class DetailBlogView(View):
    template_name = 'blog-templates/magazine-news-detail.html'

    def get(self, request, pk, slug):
        article = get_object_or_404(Article, id=pk, slug=slug, status=1)
        last_article = Article.objects.filter(status=1)[:3]

        context = {
            'article': article,
            'la': last_article
        }

        return render(request, self.template_name, context)


class ListBlogView(View):
    template_name = 'blog-templates/list-magazine.html'

    def get(self, request):
        return render(request, self.template_name)
