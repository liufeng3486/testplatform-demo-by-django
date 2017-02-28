from django.conf.urls import url
from utf_encoding import views as utf_views

urlpatterns = [
    url(r'^$',utf_views.index,name="index"),
    url(r'^add/$',utf_views.add,name="add"),
    url(r'^deUncode/$',utf_views.deUncode,name="deUncode"),

    ]
