from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# установите стандартные настройки Django для Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitelogistic.settings')

app = Celery('sitelogistic')

# Использование строки здесь означает, что работник не должен сериализовать
# объект конфигурации для дочерних процессов.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите задачи модуля задач для зарегистрированного приложения Django.
app.autodiscover_tasks()
