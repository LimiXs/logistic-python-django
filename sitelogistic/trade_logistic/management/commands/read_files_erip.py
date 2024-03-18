import os
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from trade_logistic.models import ERIPDataBase
from django.utils import timezone


class Command(BaseCommand):
    help = 'Read new files and process them'

    def handle(self, *args, **options):
        directory = r'D:\\ERIP'
        last_read_entry = ERIPDataBase.objects.order_by('-last_read_time').first()
        last_read_time = last_read_entry.last_read_time.timestamp() if last_read_entry else None

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            file_time = os.path.getctime(file_path)

            if last_read_time is None or file_time > last_read_time:
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        data = line.strip()
                        data_list = data.split('^')
                        fio = data_list[3] if data_list[3] else None

                        date = data_list[9]
                        date = datetime.strptime(date, "%Y%m%d%H%M%S") if date else None

                        erip_data = ERIPDataBase(
                            id_account=data_list[2],
                            payer_name=fio,
                            bill_pay=float(data_list[6]),
                            date=date,
                            last_read_time=timezone.now()
                        )
                        erip_data.save()
