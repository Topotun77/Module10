# Домашнее задание по теме "Многопроцессное программирование"
# Цель задания:
#
# Освоить механизмы создания процессов в Python.
# Практически применить знания, создав несколько параллельных процессов и запустив их.
#
# Задание:
# Моделирование программы для управления данными о движении товаров на складе и
# эффективной обработки запросов на обновление информации в многопользовательской среде.
#
# Представим, что у вас есть система управления складом, где каждую минуту поступают
# запросы на обновление информации о поступлении товаров и отгрузке товаров.
# Наша задача заключается в разработке программы, которая будет эффективно обрабатывать
# эти запросы в многопользовательской среде, с использованием механизма
# мультипроцессорности для обеспечения быстрой реакции на поступающие данные.
#
# Создайте класс WarehouseManager - менеджера склада, который будет обладать
# следующими свойствами:
# Атрибут data - словарь, где ключ - название продукта, а значение - его кол-во.
# (изначально пустой)
# Метод process_request - реализует запрос (действие с товаром), принимая request -
# кортеж.
# Есть 2 действия: receipt - получение, shipment - отгрузка.
# а) В случае получения данные должны поступить в data (добавить пару, если её не было
# и изменить значение ключа, если позиция уже была в словаре)
# б) В случае отгрузки данные товара должны уменьшаться (если товар есть в data и если
# товара больше чем 0).
#
# 3.Метод run - принимает запросы и создаёт для каждого свой параллельный процесс,
# запускает его(start) и замораживает(join).

import multiprocessing as mp
# from threading import Lock
import logging

class WarehouseManager():

    def __init__(self, data: dict = None):
        if not data:
            data = {}
        self.data = data

    def __str__(self):
        return str(self.data)

    def process_request(self, request: tuple, other):
        class ErrorOperation(Exception):
            def __init__(self, message='Operation Error', add_info=None):
                super().__init__()
                self.message = message
                self.add_info = add_info

        class ErrorProduct(Exception):
            def __init__(self, message='Product Error', add_info=None):
                super().__init__()
                self.message = message
                self.add_info = add_info

        def create_operation(operation):
            if operation == 'receipt':
                def operation(prod, count, other):
                    print('id(other)', id(other))
                    # with WarehouseManager.lock:
                    other.data[prod] = other.data[prod] + count if prod in other.data else count

                return operation
            elif operation == 'shipment':
                def operation(prod, count, other):
                    print('id(other)', id(other))
                    # with WarehouseManager.lock:
                    if prod in other.data:
                        other.data[prod] = other.data[prod] - count if count < other.data[prod] else 0
                    else:
                        raise ErrorProduct(f'Нет такого продукта {prod}')

                return operation
            else:
                raise ErrorOperation(f'Некорректно введена операция {operation}')

        # print('process_request!!!', id(self))
        # print(other.__dict__, id(other), id(self), self.__dict__)
        log = logging.getLogger(__name__)
        try:
            func = create_operation(request[1])
            func(request[0], request[2], other)
        except ErrorProduct as e:
            log.error(e.message)
        except ErrorOperation as e:
            log.error(e.message)
        except Exception as e:
            log.exception(e)
        print(request, ':\t', self)

    def run(self, requests):
        global queue_
        # print(id(self))
        # processes = []
        for req in requests:
            # print('in run', id(self))
            # self.process_request(req)
            # proc = mp.Process(target=WarehouseManager.process_request, kwargs=dict(self=self, request=req))
            other = self
            proc = mp.Process(target=self.process_request, kwargs=dict(request=req, other=other))
            # processes.append(proc)
            proc.start()
            proc.join()


if __name__ == '__main__':
    queue_ = mp.Queue()
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print()
    print(manager)
