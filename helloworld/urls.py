from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compress$', views.index, name='index'),
    url(r'^decompress$', views.hf_decompress, name='hf_decompress'),
    url(r'^download/(?P<file_name>[\w\.-]+)/$', views.download, name='download')
]