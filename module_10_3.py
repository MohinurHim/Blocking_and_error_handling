# Задача "Банковские операции":
import threading
import random
import time
from threading import Thread, Lock


class Bank(Thread):
    def __init__(self):
        super().__init__()
        self.balance = 0 #баланс банка (int)
        self.lock = Lock()
# Будет совершать 100 транзакций пополнения средств
    def deposit(self):
        for i in range(100):
            if self.balance >= 500 and self.lock.locked(): # Если баланс больше или равен 500 и замок lock заблокирован - lock.locked()
                self.lock.release() # разблокировать его методом release
                rand = random.randint(50, 500) # увеличение баланса на случайное целое число от 50 до 500
                self.balance += rand
                print(f"Пополнение: {rand}. Баланс: {self.balance}")
                time.sleep(0.001) # ожидание в 0.001 секунды
# Будет совершать 100 транзакций снятия
    def take(self):
        for i in range(100):
            rand_1 = random.randint(50, 500) # уменьшение баланса на случайное целое число от 50 до 500
            print(f"Запрос на {rand_1}")
            if rand_1 <= self.balance: # если случайное число меньше или равно текущему балансу
                self.balance -= rand_1 #  уменьшается balance на соответствующее число
                print(f"Снятие: {rand_1}. Баланс: {self.balance}")
            else:
                print(f"Запрос отклонён, недостаточно средств")
                self.lock.acquire() # блокировка
            time.sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')