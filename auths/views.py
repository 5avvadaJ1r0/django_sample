from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import LoginForm


class TopView(generic.TemplateView):
    template_name = 'main/index.html'


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:list')
        else:
            return super().dispatch(request, *args, **kwargs)
