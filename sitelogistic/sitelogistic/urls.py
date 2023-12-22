"""
URL configuration for sitelogistic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import threading

from django.contrib import admin
from django.urls import path, include
from trade_logistic import views
from trade_logistic.views import page_not_found
from django.apps import apps
from django.urls import include, path
from trade_logistic.scheduler import start_scheduler

if not apps.ready and not any([m.name for m in threading.enumerate() if m.name == 'apscheduler']):
    start_scheduler()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trade_logistic.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Руководство по работе с сайтом'
