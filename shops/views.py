from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  UpdateView)

from rest_framework import viewsets
from rest_framework.response import Response
from shops.forms import ShopCreateForm, ShopUpdateForm
from shops.models import Shop


class ShopBaseView(FormView):
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ShopCreateView(LoginRequiredMixin, ShopBaseView):
    template_name = 'shop/create.html'
    form_class = ShopCreateForm

    def get_success_url(self):
        return reverse('shop:list')


class ShopListView(LoginRequiredMixin, ListView):
    template_name = 'shop/list.html'
    model = Shop

    def get_queryset(self):
        return Shop.objects.filter(deleted__isnull=True)


class ShopUpdateView(LoginRequiredMixin, ShopBaseView):
    template_name = 'shop/update.html'
    form_class = ShopUpdateForm

    def get_success_url(self):
        return reverse('shop:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))

        kwargs.update({'initial': {
            'id': shop.id,
            'name': shop.name,
            'name_kana': shop.name_kana,
            'prefecture': shop.prefecture.id,
            'zip_code': shop.zip_code.id,
            'city': shop.city,
            'address1': shop.address1,
            'address2': shop.address2,
            'url': shop.url,
            'email': shop.email,
            'tel': shop.tel,
            'description': shop.description
        }})
        return kwargs


class ShopDetailView(LoginRequiredMixin, DetailView):
    template_name = 'shop/detail.html'
    model = Shop

class ShopImageView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/image.html'

class ShopViewSet(viewsets.ViewSet):

    def destroy(self, request, pk=None):
        import logging
        logging.error(pk)
        shop = Shop.objects.get(pk=pk)
        shop.deleted = timezone.now()
        shop.save()
        return Response(status=200, data=[])
