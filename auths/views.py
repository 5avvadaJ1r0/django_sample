from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse

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



