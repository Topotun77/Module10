# Домашнее задание по теме "Очереди для обмена данными между потоками."
#
# Задание:
# Моделирование работы сети кафе с несколькими столиками и потоком посетителей,
# прибывающих для заказа пищи и уходящих после завершения приема.
#
# Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду,
# занимают столик, употребляют еду и уходят. Если столик свободен, новый посетитель
# принимается к обслуживанию, иначе он становится в очередь на ожидание.
#
# Создайте 3 класса:
# Table - класс для столов, который будет содержать следующие атрибуты: number(int) -
# номер стола, is_busy(bool) - занят стол или нет.
#
# Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и
# методы:
# Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов
# (поступает из вне).
# Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
# Метод serve_customer(self, customer) - моделирует обслуживание посетителя.
# Проверяет наличие свободных столов, в случае наличия стола - начинает обслуживание
# посетителя (запуск потока), в противном случае - посетитель поступает в очередь.
# Время обслуживания 5 секунд.
# Customer - класс (поток) посетителя. Запускается, если есть свободные столы.
#
# Так же должны выводиться текстовые сообщения соответствующие событиям:
# Посетитель номер <номер посетителя> прибыл.
# Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
# Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
# Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очередь)

from threading import Thread
from queue import Queue
from time import sleep


class Table():
    def __init__(self, number: int, is_busy: bool = False):
        self.number = number
        self.is_busy = is_busy


class Cafe():
    def __init__(self, tables: list = None, customer_max=20):
        if not tables:
            self.tables = []
        else:
            self.tables = tables
        self.customer_max = customer_max
        self.queue = Queue()

    def table_not_busy(self):
        """
        Проверка свободного столика
        :return: номер свободного столика
        """
        for i in self.tables:
            if not i.is_busy:
                return i
        return None

    def customer_arrival(self):
        for i in range(1, self.customer_max + 1):
            cust = Customer(i)
            print(f'Посетитель номер {i} прибыл\n', end='')
            if not self.table_not_busy():
                print(f'Посетитель номер {i} ожидает свободный стол\n', end='')
            self.queue.put(cust)
            sleep(1)

    def serve_customer(self):
        thread_customer = []
        while True:
            tb = self.table_not_busy()
            if not tb:
                sleep(0.1)
            else:
                cust = self.queue.get()
                cust.table = tb
                cust.start()
                thread_customer.append(cust)
            if len(thread_customer) == self.customer_max and self.queue.empty():
                break
        for i in thread_customer:
            i.join()


class Customer(Thread):
    def __init__(self, number: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = number
        self.table = None

    def run(self):
        self.table.is_busy = True
        print(f'Посетитель номер {self.number} сел за стол {self.table.number}\n', end='')
        sleep(5)
        print(f'Посетитель номер {self.number} покушал и ушёл.\n', end='')
        self.table.is_busy = False


# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_serve_thread = Thread(target=cafe.serve_customer)
customer_serve_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
customer_serve_thread.join()
print('\033[93mОбслуживание всех посетителей окончено\033[0m')
