# -*- coding: utf-8 -*-

import base64
import os
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, TemplateView
from rest_framework import viewsets
from rest_framework.response import Response

from apps.settings import MEDIA_ROOT, MEDIA_URL
from shops.forms import ShopCreateForm, ShopUpdateForm
from shops.models import Shop, ShopImage
from shops.serializers import ShopImageSerializer


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))
        ctx['shop'] = shop
        return ctx

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        shop = get_object_or_404(Shop, pk=self.kwargs.get('pk'))
        ctx['shop'] = shop
        ctx['image_list'] = ShopImage.objects.filter(
            shop=shop,
            deleted__isnull=True
            ).order_by('order', 'id')
        return ctx


class ShopViewSet(viewsets.ViewSet):

    def destroy(self, request, pk=None):
        try:
            shop = Shop.objects.get(pk=pk)
            shop.deleted = timezone.now()
            shop.save()
        except Shop.DoesNotExist:
            return Response(status=403, data=[])

        return Response(status=200, data=[])


class ShopImageViewSet(viewsets.ViewSet):

    def _create_image_filename(self, filename):
        name = str(uuid.uuid4()).replace('-', '')
        extension = os.path.splitext(filename)[-1]
        return name + extension

    def update_order(self, request, pk=None):
        images = []
        if request.data:
            for row in request.data:
                image = ShopImage()
                image.id = row['id']
                image.order = row['order']
                image.updated = timezone.now()
                images.append(image)
            ShopImage.objects.bulk_update(images, fields=['order', 'updated'])
        return Response(status=200, data=[])

    def create(self, request, pk=None):
        mimetypes = ['image/jpeg', 'image/jpg', 'image/gif', 'image/png']
        if request.data['mimetype'] not in mimetypes:
            raise Http404

        filename = self._create_image_filename(request.data['filename'])
        request.data['title'] = request.data['filename']
        request.data['image'] = ContentFile(base64.b64decode(
                                            request.data['content']),
                                            name=filename)
        request.data['shop'] = Shop.objects.get(pk=pk)
        serializer = ShopImageSerializer()
        instance = serializer.create(validated_data=request.data)

        return Response(status=200, data=[instance.id])

    def list(self, request, pk=None):
        shop = get_object_or_404(Shop, pk=pk)
        rows = ShopImage.objects.filter(shop=shop, deleted__isnull=True)
        return Response(status=200, data=[row.id for row in rows])

    def retrieve(self, request, pk=None):
        no_image_path = MEDIA_ROOT + '/images/' + 'm_e_others_501.png'
        try:
            shop = Shop.objects.get(pk=pk)
            image = ShopImage.objects.filter(shop=shop, deleted__isnull=True).order_by('order')[:1]
            image = image.get()
            image_path = MEDIA_ROOT + '/' + image.image.url.replace(MEDIA_URL, '')
        except Shop.DoesNotExist:
            image_path = no_image_path
        except ShopImage.DoesNotExist:
            image_path = no_image_path

        return HttpResponse(File(open(image_path, 'rb')), content_type="image/png")

    def destroy(self, request, pk=None):
        shop_image = get_object_or_404(ShopImage, pk=pk)
        image = shop_image.image
        shop_image.deleted = timezone.now()
        shop_image.save()
        image.delete(False)
        return Response(status=200, data=[])
