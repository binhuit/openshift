from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compress$', views.index, name='index'),
    url(r'^decompress$', views.hf_decompress, name='hf_decompress'),
    url(r'^lzw-compress$', views.lzw_compress, name='lzw_index'),
    url(r'^lzw-decompress$', views.lzw_decompress, name='lzw_decompress'),
    url(r'^sf-compress$', views.sf_compress, name='sf_index'),
    url(r'^sf-decompress$', views.sf_decompress, name='sf_decompress'),
    url(r'^download/(?P<file_name>.+)/$', views.download, name='download')
]