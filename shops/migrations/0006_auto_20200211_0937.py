# Generated by Django 3.0.3 on 2020-02-11 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_shopimage_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopimage',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_image', to='shops.Shop'),
        ),
    ]
