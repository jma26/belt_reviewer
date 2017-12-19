from django.conf.urls import url
from . import views
from models import *

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.book),
    url(r'^books/add/(?P<id>\d+)$', views.add),
    url(r'^book/process/(?P<id>\d+)$', views.add_process),
    url(r'^book/user/(?P<id>\d+)$', views.user_info),
    url(r'^book/(?P<id>\d+)$', views.book_info),
    url(r'^book/comment/(?P<id>\d+)$', views.add_comment),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout)
]