from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download/(?P<file_name>[\w\.]+)/$', views.download, name='download')
]