"""
URL configuration for bookclub project.
"""

from django.contrib import admin
from django.urls import path
from books.views import SuggestBookView, IndexView
from users.views import UserCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(template_name="books/index.html"), name='index'),
    path('suggest/', SuggestBookView.as_view(), name='suggest'),
    path('account/signup/', UserCreateView.as_view(), name="signup"),
    path('account/login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login")

]

