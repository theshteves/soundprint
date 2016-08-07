from django.conf.urls import url

from . import views


app_name = 'api'

urlpatterns = [
    url(r'^api', views.api, name='encode'),
    url(r'^upload', views.upload, name='upload'),
    url(r'^', views.index, name='index')
]
