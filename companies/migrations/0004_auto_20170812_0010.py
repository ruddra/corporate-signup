# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 00:10
from __future__ import unicode_literals

import companies.services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20170812_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(upload_to=companies.services.CompanyService.get_file_path, verbose_name='Company Logo'),
        ),
    ]