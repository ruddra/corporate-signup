# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, verbose_name='Company')),
                ('logo', models.FileField(upload_to='', verbose_name='Company Logo')),
                ('description', models.TextField()),
                ('company_type', models.IntegerField(choices=[(0, 'Public Limited Company'), (1, 'Ltd.'), (2, 'Limited Partnership'), (3, 'Unlimited Partnership'), (4, 'Chartered Company'), (5, 'Statutory Company'), (6, 'Holding Company'), (7, 'Subsidiary Company'), (8, 'Sole Proprietor'), (9, 'NGOs')], default=0, help_text='Please choose from Business entities for this company', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
    ]
