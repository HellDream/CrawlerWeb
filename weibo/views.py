# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from .models import Key, Weibo
from django.shortcuts import render, get_object_or_404
from weiboCrawler2 import WeiboCrawler
from .tasks import hello_world, do_crawler
# Create your views here.


def search_page(request):
    keys = Key.objects.all().order_by("-created_time")
    title = "Weibo Search"
    context = {
        'title': title,
        'keys': keys
    }
    if request.method == 'POST':
        keyword = request.POST['key']
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            username = None
            password = None
        try:
            # crawler = WeiboCrawler(keyword=keyword, username=username, password=password)
            # crawler.search()
            do_crawler.delay(keyword, username, password)

            # time.sleep(4)
            # for key in Key.objects.filter(keyword=keyword):
            #     if not key.has_weibo:
            #         key.delete()

            keys = Key.objects.filter(keyword=keyword).order_by("-created_time")
            while not keys.exists():
                time.sleep(1)
                keys = Key.objects.filter(keyword=keyword).order_by("-created_time")

            context = {
                'title': title,
                'keys': keys
            }
            return render(request, "keywords_filter.html", context=context)

        except:
            return render(request, "search.html", context=context)

    return render(request, "search.html", context=context)


def keyword_page(request, pk):

    key = get_object_or_404(Key, pk=pk)
    title = key.keyword
    tweets = Weibo.objects.filter(key=key)

    context = {
        'key': key,
        'tweets': tweets,
        'title': title
    }
    return render(request, "keyword.html", context)


def get_map(request, pk):
    weibo_obj = Weibo.objects.get(pk=pk)
    dot = "·"
    title = weibo_obj.key.keyword
    try:
        locations = weibo_obj.location.split(dot)
        location = locations[0]
        print location
    except:
        locations = None
        location = None
    context = {
        'weibo': weibo_obj,
        'locations': str(weibo_obj.location),
        'location': location,
        'title': title
    }
    return render(request, "map.html", context)


def show_all_map(request):
    tweets = Weibo.objects.filter(location__isnull=False).order_by("-found_time")
    title = "All Location"
    context = {
        "tweets": tweets,
        "title": title
    }
    return render(request, "allmap.html", context)