from logging import getLogger
from django.apps import AppConfig


class TradeLogisticConfig(AppConfig):
    verbose_name = 'Доступные модули'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trade_logistic'


logger = getLogger('django')

