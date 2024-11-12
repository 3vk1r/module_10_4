import threading as thr
from random import randint as rnt
from time import sleep as sp
from queue import Queue as Q

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(thr.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time = rnt(3,10)
        sp(time)

class Cafe:
    def __init__(self, *tables: Table):
        self.tables = tables
        self.queue = Q()

    def guest_arrival(self, *guests: Guest):
        for guest in guests:
            free_table = False
            for table in self.tables:
                if not table.guest:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел за стол номер {table.number}')
                    free_table = True
                    break
            if not free_table:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not(self.queue.empty() and (not any(t.guest for t in self.tables))):
            for table in self.tables:
                if not table.guest:
                    if not self.queue.empty():
                        table.guest = self.queue.get()
                        print(f'{table.guest.name} вышел(-ла) из очереди',
                              f'и сел(-а) за стол номер {table.number}')
                        table.guest.start()
                else:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                        print(f'Стол номер {table.number} свободен')
                        table.guest = None


tables = [Table(number) for number in range(1, 6)]

guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
                    'Alexandra']
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()