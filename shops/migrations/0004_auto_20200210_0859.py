# Generated by Django 3.0.3 on 2020-02-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_auto_20200205_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopimage',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shopimage',
            name='title',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='shopimage',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
