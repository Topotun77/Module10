# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# TODO Внимание! это задание можно выполнять только после зачета lesson_012/02_volatility_with_threads.py !!!

# TODO тут ваш код в многопроцессном стиле

from os import walk, path
import csv
import logging
from multiprocessing import Process
from time import time


# from pprint import pprint

class TickerReader(Process):

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # log = logging.getLogger(__name__)
        with open(self.file_path, newline='') as cf:
            data_ = csv.reader(cf)
            price_list = []
            for row in data_:
                try:
                    price_list.append(float(row[2]))
                except Exception as e:
                    # log.error(e.args)
                    pass
            tick_name = row[0]
            price_list.sort()
            # print(price_list)
            average_price = (price_list[0] + price_list[-1]) / 2
            volatility = ((price_list[-1] - price_list[0]) / average_price) * 100
            # print(f'{tick_name} волатильность {volatility}')
            print(id(self), id(TickerReader), id(Tickers.TickerData))  # TODO id все время разные!!!
            Tickers.TickerData[tick_name] = volatility
            print(Tickers.TickerData)


class Tickers():
    TickerData: dict = {}

    def __init__(self, path_='.'):
        self.path_ = path_

    def print_rez(self, data):
        """
        Печать результата в формате:
            Максимальная волатильность:
            ТИКЕР1 - ХХХ.ХХ %
            ТИКЕР2 - ХХХ.ХХ %
            ТИКЕР3 - ХХХ.ХХ %
        Минимальная волатильность:
            ТИКЕР4 - ХХХ.ХХ %
            ТИКЕР5 - ХХХ.ХХ %
            ТИКЕР6 - ХХХ.ХХ %
        Нулевая волатильность:
            ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
        Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
        :param data: Словарь с данными для вывода
        :return: None
        """
        log = logging.getLogger(__name__)
        # ticker_list = list(map(lambda x, y: [y, x], data.keys(), data.values()))
        ticker_list = list(zip(data.values(), data.keys()))
        ticker_list.sort()
        zero_list = []
        while ticker_list and ticker_list[0][0] == 0:
            zero_list.append(ticker_list[0][1])
            ticker_list.pop(0)
        zero_list.sort()
        try:
            print('\nМаксимальная волатильность:')
            for i in range(3):
                print(
                    f'\t{ticker_list[len(ticker_list) - i - 1][1]} - {ticker_list[len(ticker_list) - i - 1][0]:0.2f} %')
            print('\nМинимальная волатильность:')
            for i in range(3):
                print(f'\t{ticker_list[2 - i][1]} - {ticker_list[2 - i][0]:0.2f} %')
        except Exception as e:
            log.error(e.args)
        print('\nНулевая волатильность:')
        print(', '.join(zero_list))

    def main(self):
        """
        Основной процесс
        :return: None
        """
        path_ = path.abspath(self.path_)
        processes = []
        for dir_, _, files in walk(path_):
            print('\nСписок файлов для обработки:', files)
            for fl_ in files:
                filepath = path.join(dir_, fl_)
                print(f'Обнаружен файл: {fl_}, обрабатываем...')
                ps = TickerReader(filepath)
                ps.start()
                processes.append(ps)
        for tr in processes:
            tr.join()
        self.print_rez(Tickers.TickerData)


if __name__ == '__main__':
    time_start = time()
    ticker = Tickers('./trades/')
    ticker.main()
    time_end = time()
    print(f'\nОбработка производилась: {time_end - time_start} сек.')
