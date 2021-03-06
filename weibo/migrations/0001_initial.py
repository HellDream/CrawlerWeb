# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(default='', max_length=200)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weibo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=500)),
                ('content', models.TextField(blank=True)),
                ('timestamp', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('found_time', models.DateTimeField(auto_now_add=True)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weibo.Key')),
            ],
        ),
    ]
