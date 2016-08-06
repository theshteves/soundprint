from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^decode', views.decode, name='decode'),
    url(r'^encode', views.encode, name='encode'),
    url(r'^', views.index, name='index')
]
