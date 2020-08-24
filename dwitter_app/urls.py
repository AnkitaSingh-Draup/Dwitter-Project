from django.contrib import admin
from django.urls import path
from django.conf.urls import  url
from .views import *


urlpatterns = [
    url('dweets/', dweets),
    url(r'^dweets_edit/(?P<pk>.+)',dweets_edit),
    url('search_follow/',search_follow),
    url(r'like/(?P<pk>.+)', like),
    url(r'comment/(?P<pk>.+)', comment),
    url('search_dweet/',search_dweet),
]