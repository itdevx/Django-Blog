from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from .forms import SignInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class SignUpBlogView(View):
    template_name = 'authenticate-templates/sign-up.html'

    def get(self, request):
        return render(request, self.template_name)


class SignInBlogView(View):
    template_name = 'authenticate-templates/sign-in.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class()
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


class SignUpBlogView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('blog:index')
    template_name = 'authenticate-templates/sign-up.html'


class SignOutBlogView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:index')
        

class DashboardBlogView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)



