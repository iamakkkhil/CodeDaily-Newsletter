# Generated by Django 3.2.5 on 2021-08-01 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20210731_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='space_cmplx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='time_cmplx',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
