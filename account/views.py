from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponse
from .forms import SignInForm, SignUpForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from .mixins import FormValidMixins, FieldsMixins
from blog.models import Article
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
from blog.models import Category
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from account.tokens import account_activation_token
from django.utils.encoding import force_str as force_text
from django.utils.encoding import force_bytes


class SignInBlogView(View):
    template_name = 'authenticate-templates/sign-in.html'
    form_class = SignInForm

    def get(self, request):
        """send data for template. """
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'date': jalali_converter(datetime.datetime.now())})

    def post(self, request):
        """post user data and login. """
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
        return render(request, self.template_name, {'form': form, 'date': jalali_converter(datetime.datetime.now())})


# class SignUpBlogView(CreateView):
#     form_class = SignUpForm
#     template_name = 'authenticate-templates/sign-up.html'

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = 'فعال سازی اکانت'
#         message = render_to_string('authenticate-templates/acc_verify_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#             mail_subject, message, to=[to_email]
#         )
#         email.send()
#         return HttpResponse('لینک فعالسازی برای ایمیل شما ارسال شد!')
        
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponse('ممنون از ثبت نام شما!')
#     else:
#         return HttpResponse('لینک فعالسازی منقضی شده است!')
        
class SignUpBlogView(CreateView):
    form_class = SignUpForm
    template_name = 'authenticate-templates/sign-up.html'

    def form_valid(self, form):
        """
        checking form valid for register user and login after registering.
        """
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('blog:index')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """send date value for tempalte. """
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        return context


class SignOutBlogView(View):
    def get(self, request):
        """logout user. """
        logout(request)
        return redirect('blog:index')


class DashboardBlogView(LoginRequiredMixin, View):
    login_url = 'account:sign-in'
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        """checking the superuser or user and filtering the fields. """
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['article'] = Article.objects.filter(status=1)
        return context


class UpdateArticle(LoginRequiredMixin, FieldsMixins, UpdateView):
    model = Article
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-article.html'
    login_url = 'account:sign-in'

    def get_queryset(self):
        """filter users based on superuser or article author. """
        if self.request.user == Article.author or self.request.user.is_superuser:
            return super().get_queryset()
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.filter(status=1)
        context['date'] = jalali_converter(datetime.datetime.now())
        return context


class DeleteArticle(LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/delete-article.html'
    success_url = reverse_lazy('account:dashboard')
    login_url = 'account:sign-in'
    context_object_name = 'a'   

    def get_queryset(self):
        """user filtering based on superuser. """
        if self.request.user.is_superuser:
            return Article.objects.filter(id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.filter(status=1)
        context['date'] = jalali_converter(datetime.datetime.now())
        return context


class CreateCategory(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['category_name']
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/create-category.html'
    login_url = 'account:sign-in'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['category'] = Category.objects.all()
        context['article'] = Article.objects.filter(status=1)
        return context

    def dispatch(self, request, *args, **kwargs):
        """filter this page by superuser. """
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()


class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__' 
    success_url = reverse_lazy('account:create-category')
    template_name = 'dashboard/update-category.html'
    login_url = 'account:sign-in'
    slug_field = 'category_slug'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['article'] = Article.objects.filter(status=1)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dashboard/delete-category.html'
    success_url = reverse_lazy('account:create-category')
    login_url = 'account:sign-in'
    context_object_name = 'category'   
    slug_field = 'category_slug'
    slug_url_kwarg = 'category_slug'

    # def get_queryset(self):
    #     """user filtering based on superuser. """
    #     if self.request.user.is_superuser:
    #         return Article.objects.filter(id=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
    #     else:
    #         raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.filter(status=1)
        context['date'] = jalali_converter(datetime.datetime.now())
        return context


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('account:dashboard')
    template_name = 'dashboard/update-profile.html'
    login_url = 'account:sign-in'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        """filter users by superuser or user_id after authentication. """
        if self.request.user.is_superuser:
            return super().get_queryset()
        else:
            return User.objects.filter(id=self.request.user.id)

    def dispatch(self, request, *args, **kwargs):
        """filtering fields by superuser or user. """
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['article'] = Article.objects.filter(status=1)
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['article'] = Article.objects.filter(status=1)
        return context


class AllUserDashboard(View):
    template_name = 'dashboard/users.html'
    def get(self, request):
        """show all user and filter users by superuser. """
        if request.user.is_superuser:
            users = User.objects.order_by('-id').all()
            paginator = Paginator(users, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            raise Http404()
        return render(request, self.template_name, {'users': page_obj, 'date': jalali_converter(datetime.datetime.now()), 'article': Article.objects.filter(status=1)})


class EditUserDashboard(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'dashboard/edit-user.html'
    success_url = reverse_lazy('account:all-users')
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, username, *args, **kwargs):
        """filter this page to view by superuser. """
        user = get_object_or_404(User, username=username)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = jalali_converter(datetime.datetime.now())
        context['article'] = Article.objects.filter(status=1)
        return context
        

class DeleteUserDashboard(DeleteView):
    model = User
    template_name = 'dashboard/delete-user.html'
    success_url = reverse_lazy('account:all-users')
    login_url = 'account:sign-in'
    context_object_name = 'user'   
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, username, *args, **kwargs):
        """filter this page to view by superuser. """
        user = get_object_or_404(User, username=username)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.filter(status=1)
        context['date'] = jalali_converter(datetime.datetime.now())
        return context
