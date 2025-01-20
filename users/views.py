from django.shortcuts import render
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm


class UserCreateView(CreateView):
    template_name = "users/create.html"
    form_class = CustomUserCreationForm

