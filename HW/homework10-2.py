# Домашнее задание по теме "Потоки на классах"
# Задание: Потоки на классах в Python
#
# Цель задания:
# Освоить механизмы создания и потоков в Python.
# Практически применить знания, создав класс наследника от Thread и запустив его в потоке.
#
# Инструкции:
# Напишите программу с использованием механизмов многопоточности, которая создает два
# потока-рыцаря.
#
# Каждый рыцарь должен иметь имя (name) и умение(skill). Умение рыцаря определяет,
# сколько времени потребуется рыцарю, чтобы выполнить свою защитную миссию для
# королевства.
# Враги будут нападать в количестве 100 человек. Каждый день рыцарь может ослабить
# вражеское войско на skill-человек.
# Если у рыцаря skill равен 20, то защищать крепость он будет 5 дней (5 секунд в программе).
# Чем выше умение, тем быстрее рыцарь защитит королевство.

from threading import Thread
from time import sleep

class Knight(Thread):

    def __init__(self, name, skill, enemy=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.skill = skill
        self.enemy = enemy


    def run(self):
        print(f'\033[93m{self.name}, на нас напали!\033[0m\n', end='')
        day = 0
        while self.enemy > 0:
            day += 1
            self.enemy = self.enemy - self.skill if self.enemy > self.skill else 0
            print(f'{self.name}, сражается {day} день(дня)..., осталось {self.enemy} воинов.\n', end='')
            sleep(1)
        print(f'\033[93m{self.name} одержал победу спустя {day} дней!\033[0m\n', end='')

knight1 = Knight("Sir Lancelot", 10) # Низкий уровень умения
knight2 = Knight("Sir Galahad", 20) # Высокий уровень умения
knight1.start()
knight2.start()
knight1.join()
knight2.join()
print('Все битвы закончились!')