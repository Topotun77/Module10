# Домашнее задание по теме "Создание потоков".
# Цель задания:
#
# Освоить механизмы создания потоков в Python.
# Практически применить знания, создав и запустив несколько потоков.
#
# Задание:
# Напишите программу, которая создает два потока.
# Первый поток должен выводить числа от 1 до 10 с интервалом в 1 секунду.
# Второй поток должен выводить буквы от 'a' до 'j' с тем же интервалом.
# Оба потока должны работать параллельно.

from threading import Thread
from time import sleep

def func1(n_end, n_start=1, time_=1):
    """
    Вывод чисел от n_start до n_end с задержкой time_
    :param n_start: начальное число
    :param n_end: конечное число
    :param time_: задержка
    :return: None
    """
    for i in range(n_start, n_end+1):
        print(i)
        sleep(time_)


def func2(c_start, c_end, time_=1):
    """
    Вывод символов от c_start до c_end с задержкой time_
    :param c_start: начальный символ
    :param c_end: конечный символ
    :param time_: задержка в секундах
    :return: None
    """
    code_start = ord(c_start)
    code_end = ord(c_end)
    for i in range(code_start, code_end+1):
        print(chr(i))
        sleep(time_)


thread1 = Thread(target=func1, args=(10,))
thread2 = Thread(target=func2, kwargs=dict(c_start='a', c_end='j'))

thread1.start()
thread2.start()