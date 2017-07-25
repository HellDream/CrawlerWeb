from django.conf.urls import url, include
from .views import search_page, keyword_page, get_map, show_all_map
urlpatterns = [
    url(r'^$', search_page, name="search"),
    url(r'^keyword/(?P<pk>[\d-]+)/$', keyword_page, name="keyword"),
    url(r'^weibo/(?P<pk>[\d-]+)/$', get_map, name="map"),
    url(r'^all-location/$', show_all_map, name="all_map"),

]
