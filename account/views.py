from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.http import Http404
from .forms import SignInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from .mixins import FormValidMixins, FieldsMixins
from blog.models import Article, Category
from extentions.utils import jalali_converter
import datetime
from django.core.paginator import Paginator
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
        

class DashboardBlogView(LoginRequiredMixin, View):
    login_url = 'account:sign-in'
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


class CreateArticle(LoginRequiredMixin, FormValidMixins, FieldsMixins, CreateView):
    model = Article
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/create-article.html'
    login_url = 'account:sign-in'


class UpdateArticle(LoginRequiredMixin, FieldsMixins, UpdateView):
    model = Article
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-article.html'
    login_url = 'account:sign-in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.all()
        return context


# bug
class DeleteArticle(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/delete-article.html'
    success_url = reverse_lazy('account:dashboard')
    login_url = 'account:sign-in'
    context_object_name = 'a'   

    def get_queryset(self):
        return Article.objects.filter(id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.all()
        return context



class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-profile.html'
    login_url = 'account:sign-in'

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
                'first_name',
                'last_name',
                'bio',
                'linkedin',
                'instagram',
                'twitter',
                'githb',
                'telegram'
            ]
        return super().dispatch(request, *args, **kwargs)


class ChangePassword(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/change-password.html'
    login_url = 'account:sign-in'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class AllUserDashboard(View):
    template_name = 'dashboard/users.html'

    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()
            context = {
                'users': users
            }
        else:
            raise Http404()

        return render(request, self.template_name, context)
        