# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Key(models.Model):

    keyword = models.CharField(max_length=200, default='')
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.keyword

    @property
    def get_key_weibo(self):
        instance = self
        queryset = Weibo.objects.filter(key=instance)
        return queryset

    @property
    def has_weibo(self):
        instance = self
        queryset = Weibo.objects.filter(key=instance).exists()
        if queryset:
            return True
        return False


class Weibo(models.Model):
    key = models.ForeignKey(Key)
    username = models.CharField(max_length=500, default='')
    content = models.TextField(blank=True)
    timestamp = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    found_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        string = str(self.key) + str(self.username)
        return string

