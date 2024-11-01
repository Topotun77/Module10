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

from multiprocessing import Process, Lock
import queue
import logging

class WarehouseManager():
    # lock = Lock()

    def __init__(self, data: dict = None):
        if not data:
            data = {}
        self.data = data
        self.lock = Lock()

    def __str__(self):
        return str(self.data)

    def process_request(self, request: tuple, queue_data):
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
                def operation(prod, count, queue_data):
                    with self.lock:
                        data = queue_data.get()
                        data[prod] = data[prod] + count if prod in data else count
                        queue_data.put(data)

                return operation
            elif operation == 'shipment':
                def operation(prod, count, queue_data):
                    with self.lock:
                        data = queue_data.get()
                        if prod in data:
                            data[prod] = data[prod] - count if count < data[prod] else 0
                            queue_data.put(data)
                        else:
                            queue_data.put(data)
                            raise ErrorProduct(f'Нет такого продукта {prod}')


                return operation
            else:
                raise ErrorOperation(f'Некорректно введена операция {operation}')

        log = logging.getLogger(__name__)
        try:
            func = create_operation(request[1])
            func(request[0], request[2], queue_data)
        except ErrorProduct as e:
            log.error(e.message)
        except ErrorOperation as e:
            log.error(e.message)
        except Exception as e:
            log.exception(e)
        print(request, ':\t', self)

    def run(self, requests, queue_data):
        processes = []
        for req in requests:
            queue_data.put(self.data)
            # self.process_request(req)
            proc = Process(target=WarehouseManager.process_request(self, req, queue_data))
            # proc = Process(target=self.process_request, kwargs=dict(request=req, queue_data=queue_data))
            self.data = queue_data.get()
            processes.append(proc)
        for i in processes:
            i.start()
            i.join()


if __name__ == '__main__':
    queue_ = queue.Queue(maxsize=10)
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
    manager.run(requests, queue_)

    # Выводим обновленные данные о складских запасах
    print()
    print(manager)