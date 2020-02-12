# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Prefecture(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = 'prefecture'


class Zipcode(models.Model):
    id  = models.CharField(primary_key=True, max_length=7, db_index=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, db_index=True)
    address = models.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = 'zip_code'


class Shop(models.Model):
    name = models.CharField(max_length=255, db_index=True, null=False, blank=True)
    name_kana = models.CharField(max_length=255, null=False, blank=True)
    zip_code = models.ForeignKey(Zipcode, on_delete=models.CASCADE, null=False, blank=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=False, blank=True)
    city = models.CharField(max_length=255, db_index=True, null=False, blank=True)
    address1 = models.CharField(max_length=255, db_index=True, null=False, blank=True)
    address2 = models.CharField(max_length=255, db_index=True, null=False, blank=True)
    url = models.URLField(max_length=1024, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'shop'


class ShopImage(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_image")
    title = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='images/')
    order = models.IntegerField(default=1)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'shop_image'
