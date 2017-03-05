from django.conf.urls import url
from vgc import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]