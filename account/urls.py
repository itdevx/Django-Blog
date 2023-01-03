from django.urls import path
from .views import SignUpBlogView, DashboardBlogView, SignInBlogView, SignOutBlogView

app_name = 'account'


urlpatterns = [
    path(
        'sign-up/', SignUpBlogView.as_view(), name='sign-up'
    ),
    path(
        'dashboard/', DashboardBlogView.as_view(), name='dashboard'
    ),
    path(
        'sign-in/', SignInBlogView.as_view(), name='sign-in'
    ),
    path(
        'sign-out/', SignOutBlogView.as_view(), name='sign-out'
    )
]