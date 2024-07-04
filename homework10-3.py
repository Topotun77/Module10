# Домашнее задание по теме "Блокировки потоков для доступа к общим данным"
# Цель задания:
# Практически применить знания о механизмах блокировки потоков в Python, используя класс Lock
# из модуля threading.
#
# Задание:
# Реализуйте программу, которая имитирует доступ к общему ресурсу с использованием механизма
# блокировки потоков.
#
# Класс BankAccount должен отражать банковский счет с балансом и методами для пополнения и
# снятия денег. Необходимо использовать механизм блокировки, чтобы избежать проблемы гонок
# (race conditions) при модификации общего ресурса.

from threading import Thread, Lock
# from time import sleep

class BankAccount():
    lock = Lock()
    def __init__(self, balance=1000):
        self.balance = balance

    def deposit(self, amount):
        with BankAccount.lock:
            self.balance += amount
            print(f'Deposited {amount}, new balance is {self.balance}')
        # sleep(1)

    def withdraw(self, amount):
        with BankAccount.lock:
            self.balance -= amount
            print(f'Withdrew {amount}, new balance is {self.balance}')

def deposit_task(account, amount):
    for _ in range(5):
        account.deposit(amount)

def withdraw_task(account, amount):
    for _ in range(5):
        account.withdraw(amount)

account = BankAccount()

deposit_thread = Thread(target=deposit_task, args=(account, 100))
withdraw_thread = Thread(target=withdraw_task, args=(account, 150))

deposit_thread.start()
withdraw_thread.start()

deposit_thread.join()
withdraw_thread.join()
