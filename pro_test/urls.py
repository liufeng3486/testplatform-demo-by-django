"""pro_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from manage_app import views as manage_views
import settings
import time
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',manage_views.index),
    url(r'^test1/',include('test1.urls')),
    url(r'^utf/',include('utf_encoding.urls')),
    url(r'^md5/',include('md5_encoding.urls')),
    # url(r'^auto_py/',include('auto_py.urls'))  stripping pro
    # url(r'^testCaseApp/',include('testCaseApp.urls')), stripping pro
    # url(r'^log_test/',include('log_test.urls')), stripping pro
    #url(r'^staticfiles/(?P<path>.*)$','django.views.static.serve',{'document_root':'/css/style.css', 'show_indexes': True}),
  #  url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),
]
