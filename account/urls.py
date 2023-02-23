from django.urls import path
from .views import (
    SignUpBlogView,
    DashboardBlogView,
    SignInBlogView,
    SignOutBlogView,
    CreateArticle,
    UpdateArticle,
    DeleteArticle,
    UpdateProfile,
    ChangePassword,
    AllUserDashboard,
    EditUserDashboard,
    DeleteUserDashboard,
    CreateCategory,
    UpdateCategory,
    DeleteCategory
    )

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
    ),
    path(
        'dashboard/create-article/', CreateArticle.as_view(), name='create-article'
    ),
    path(
        'dashboard/create-category/', CreateCategory.as_view(), name='create-category'
    ),
    path(
        'dashboard/update-category/<category_slug>', UpdateCategory.as_view(), name='update-category'
    ),
    path(
        'dashboard/delete-category/<category_slug>', DeleteCategory.as_view(), name='delete-category'
    ),
    path(
        'dashboard/update-article/<int:pk>/', UpdateArticle.as_view(), name='update-article'
    ),
    path(
        'dashboard/delete-article/<pk>/<slug>', DeleteArticle.as_view(), name='delete-article'
    ),
    path(
        'dashboard/update-profile/@<username>', UpdateProfile.as_view(), name='update-profile'
    ),
    path(
        'dashboard/change-password/', ChangePassword.as_view(), name='change-password'
    ),
    path(
        'dashboard/all-users', AllUserDashboard.as_view(), name='all-users'
    ),
    path(
        'dashboard/edit-user/@<username>/', EditUserDashboard.as_view(), name='edit-user'
    ),
    path(
        'dashboard/delete-user/@<username>/', DeleteUserDashboard.as_view(), name='delete-user'
    )
]