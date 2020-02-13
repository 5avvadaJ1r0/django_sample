# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EmailValidator, URLValidator
from django.utils import timezone

from shops.models import Prefecture, Shop, Zipcode


class ShopBaseForm(forms.Form):
    prefecture_choices = Prefecture.objects.values_list('id', 'name').order_by('id')
    prefecture_choices = ((prefecture_choice[0], prefecture_choice[1]) for prefecture_choice in prefecture_choices)
    prefecture = forms.ChoiceField(widget=forms.Select(), choices=prefecture_choices)

    name = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    name_kana = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    zip_code = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    city = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    address1 = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    address2 = forms.CharField(max_length = 40, widget=forms.TextInput(attrs={'size':40}))
    url = forms.CharField(max_length = 1024, required=False, widget=forms.TextInput(attrs={'size':60}))
    email = forms.CharField(max_length = 1024, required=False, widget=forms.TextInput(attrs={'size':40}))
    tel = forms.CharField(max_length = 1024, widget=forms.TextInput(attrs={'size':40}))
    description = forms.CharField(max_length = 1024, required=False, widget=forms.Textarea(attrs={'col':50, 'row':4}))

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        zip_code = zip_code.replace('-', '')
        try:
            Zipcode.objects.get(id=zip_code)
        except  ObjectDoesNotExist:
            raise forms.ValidationError('郵便番号が不正です')

        return zip_code

    def clean_name_kana(self):
        name_kana = self.cleaned_data['name_kana']
        if name_kana:
            pattern = re.compile(r'[\u30A1-\u30F4]+')
            if not pattern.fullmatch(name_kana):
                raise forms.ValidationError('店舗名（カナ）はカタカナを入力してください')
        return name_kana

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        tel = tel.replace('-', '')
        if tel:
            pattern = re.compile(r'\d{10,11}$')
            if not pattern.fullmatch(tel):
                raise forms.ValidationError('電話番号は半角数字を入力してください')
        return tel

    def clean_email(self):
        if self.cleaned_data['email']:
            validator = EmailValidator()
            validator(self.cleaned_data['email'])
        return self.cleaned_data['email']

    def clean_url(self):
        if self.cleaned_data['url']:
            validator = URLValidator()
            validator(self.cleaned_data['url'])
        return self.cleaned_data['url']

class ShopCreateForm(ShopBaseForm):

    def save(self):
        Shop.objects.create(
            name=self.cleaned_data['name'],
            name_kana=self.cleaned_data['name_kana'],
            prefecture_id=self.cleaned_data['prefecture'],
            zip_code_id=self.cleaned_data['zip_code'],
            city=self.cleaned_data['city'],
            address1=self.cleaned_data['address1'],
            address2=self.cleaned_data['address2'],
            url=self.cleaned_data['url'],
            email=self.cleaned_data['email'],
            tel=self.cleaned_data['tel'],
            description=self.cleaned_data['description']
        )


class ShopUpdateForm(ShopBaseForm):
    id = forms.IntegerField(widget = forms.HiddenInput())

    def save(self):
        Shop.objects.update(
            id=self.cleaned_data['id'],
            name=self.cleaned_data['name'],
            name_kana=self.cleaned_data['name_kana'],
            prefecture_id=self.cleaned_data['prefecture'],
            zip_code_id=self.cleaned_data['zip_code'],
            city=self.cleaned_data['city'],
            address1=self.cleaned_data['address1'],
            address2=self.cleaned_data['address2'],
            url=self.cleaned_data['url'],
            email=self.cleaned_data['email'],
            tel=self.cleaned_data['tel'],
            description=self.cleaned_data['description'],
            updated=timezone.now()
        )
