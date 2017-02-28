from django.conf.urls import url
from md5_encoding import views as md5_views

urlpatterns = [
    url(r'^$',md5_views.index,name="index"),
    url(r'^md5/$',md5_views.md5,name="add"),
    ]
