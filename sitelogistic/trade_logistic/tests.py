import time
from django.test import TestCase


# Create your tests here.
def measure_execution_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    print(f"Время выполнения функции: {end_time - start_time} секунд.")
