# Generated by Django 3.0.3 on 2020-02-05 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20200204_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
