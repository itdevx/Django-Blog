from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import User
from blog.models import Article


class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control m-2'})
        self.fields['email'].widget.attrs.update({'class':'form-control m-2'})
        self.fields['image'].widget.attrs.update({'class':'form-control m-2'})
        self.fields['bio'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'بیوگرافی درباره خودتان:'})
        self.fields['linkedin'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'آدرس لینکدین خودرا وارد کنید'})
        self.fields['instagram'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'آدرس اینستاگرام خودرا وارد کنید'})
        self.fields['twitter'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'آدرس توئیتر خودرا وارد کنید'})
        self.fields['githb'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'آدرس گیت هاب خودرا وارد کنید'})
        self.fields['telegram'].widget.attrs.update({'class':'form-control m-2', 'placeholder':'آدرس تلگرام خودرا وارد کنید'})

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
        if user.is_superuser:
            self.fields['password'].disabled = True


    class Meta:
        model = User
        fileds = ['username', 'email', 'image', 'bio', 'linkedin' ,'instagram', 'twitter', 'githb', 'telegram']
        exclude = ()
