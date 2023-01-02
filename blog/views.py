from django.shortcuts import render
from django.views.generic import ListView, View, DetailView


class IndexView(View):
    template_name = 'blog-templates/index-magazine.html'

    def get(self, request):
        return render(request, self.template_name)


class DetailBlogView(View):
    template_name = 'blog-templates/magazine-news-detail.html'

    def get(self, request):
        return render(request, self.template_name)


class ListBlogView(View):
    template_name = 'blog-templates/list-magazine.html'

    def get(self, request):
        return render(request, self.template_name)
