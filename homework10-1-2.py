# Домашнее задание по теме "Создание потоков".
# Цель: понять как работают потоки на практике, решив задачу
#
# Задача "Потоковая запись в файлы":
# Необходимо создать функцию wite_words(word_count, file_name), где word_count -
# количество записываемых слов, file_name - название файла, куда будут записываться
# слова.
# Функция должна вести запись слов "Какое-то слово № <номер слова по порядку>" в
# соответствующий файл с прерыванием после записи каждого на 0.1 секунду.
# Сделать паузу можно при помощи функции sleep из модуля time, предварительно импортировав её: from time import sleep.
# В конце работы функции вывести строку "Завершилась запись в файл <название файла>".
#
# После создания файла вызовите 4 раза функцию wite_words, передав в неё следующие
# значения:
# 1. 10, example1.txt
# 2. 30, example2.txt
# 3. 200, example3.txt
# 4. 100, example4.txt
#
# После вызовов функций создайте 4 потока для вызова этой функции со следующими
# аргументами для функции:
# 1. 10, example5.txt
# 2. 30, example6.txt
# 3. 200, example7.txt
# 4. 100, example8.txt
#
# Запустите эти потоки методом start не забыв, сделать остановку основного потока
# при помощи join.
# Также измерьте время затраченное на выполнение функций и потоков. Как это сделать
# рассказано в лекции к домашнему заданию.

from threading import Thread
from time import sleep, time

def wite_words(word_count, file_name):
    """
    Запись слов "Какое-то слово № <номер слова по порядку>" в соответствующий файл с
    прерыванием после записи каждого на 0.1 секунду.
    :param word_count: количество записываемых слов
    :param file_name: название файла, куда будут записываться слова
    :return:
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as fl:
            for i in range(word_count):
                fl.write(f'Какое-то слово № {i}\n')
                sleep(0.1)
    except Exception as err:
        print(f'Ошибка при записи файла\n{err.args}')
    else:
        print(f'Завершилась запись в файл {file_name}')


time_start = time()

wite_words(10, 'example1.txt')
wite_words(30, 'example2.txt')
wite_words(200, 'example3.txt')
wite_words(100, 'example4.txt')

time_end = time()
print(f'Время выполнения: {(time_end-time_start):.6f}\n')

time_start = time()

tr1 = Thread(target=wite_words, args=(10, 'example5.txt'))
tr2 = Thread(target=wite_words, args=(30, 'example6.txt'))
tr3 = Thread(target=wite_words, args=(200, 'example7.txt'))
tr4 = Thread(target=wite_words, args=(100, 'example8.txt'))

tr1.start()
tr2.start()
tr3.start()
tr4.start()

tr1.join()
tr2.join()
tr3.join()
tr4.join()

time_end = time()
print(f'Время выполнения с потоками: {(time_end-time_start):.6f}')
