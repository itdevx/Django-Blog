from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView
from .forms import SignInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from .mixins import FormValidMixins, FieldsMixins
from blog.models import Article, Category
from extentions.utils import jalali_converter
import datetime
from django.core.paginator import Paginator
from .models import User


class SignUpBlogView(View):
    template_name = 'authenticate-templates/sign-up.html'

    def get(self, request):
        return render(request, self.template_name)


class SignInBlogView(View):
    template_name = 'authenticate-templates/sign-in.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('blog:index')
            else:
                form.add_error('username', 'نام کاربری یا کلمه عبور اشتباه میباشد')
        return render(request, self.template_name, {'form': form})
        


class SignUpBlogView(CreateView):
    form_class = SignUpForm
    template_name = 'authenticate-templates/sign-up.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('blog:index')
        return super().form_valid(form)


class SignOutBlogView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:index')
        

class DashboardBlogView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        if request.user.is_superuser:
            article = Article.objects.order_by('-date').all()
            paginator = Paginator(article, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            article = Article.objects.filter(author=request.user)
            paginator = Paginator(article, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'article': page_obj, 'date': jalali_converter(datetime.datetime.now())})


class CreateArticle(FormValidMixins, FieldsMixins, CreateView):
    model = Article
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/create-article.html'


class UpdateArticle(FieldsMixins, UpdateView):
    model = Article
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.all()
        return context
    

# bug
class DeleteArticle(DeleteView):
    model = Article
    success_url = reverse_lazy('account:dashboard')


class UpdateProfile(UpdateView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-profile.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return User.objects.filter(id=self.request.user.id)
            
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = '__all__'
        else:
            self.fields = [
                'username',
                'email',
                'image',
                'bio',
                'linkedin',
                'instagram',
                'twitter',
                'githb',
                'telegram'
            ]
        return super().dispatch(request, *args, **kwargs)

