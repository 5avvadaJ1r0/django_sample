# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import redirect

class TopPageView(TemplateView):
    template_name = 'app/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:list')
        else:
            return super().dispatch(request, *args, **kwargs)

