import sys

from logging import getLogger
from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.db.models import Q


class TradeLogisticConfig(AppConfig):
    verbose_name = 'Доступные модули'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trade_logistic'


logger = getLogger('django')


class CustomAdminConfig(AdminConfig):

    def ready(self):
        super().ready()
        if 'process_tasks' not in sys.argv:
            return
        from tasks import my_task
        self._run_task(my_task)
        # self._run_task(custom_bgtask2)

    def _run_task(self, task_func):
        from background_task.models import Task
        q_locked = Q(locked_at__isnull=False) | Q(locked_by__isnull=False)
        Task.objects.filter(task_name=task_func.name).filter(q_locked).delete()
        if not Task.objects.filter(task_name=task_func.name).exists():
            logger.info('Созданиe фоновой задачи %s', task_func.name)
            task_func()
