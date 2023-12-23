from colors import Colors
from sqlite import *


class Record:
    def __init__(self):
        self.numbers = []
        self.max = 10
        self.real_max = 0
        create_table(self.numbers)
        connection = sql.connect('records.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM records')
        records = cursor.fetchall()
        if not records:
            self.numbers = [0 for i in range(11)]
        else:
            for row in records:
                self.numbers.append(row[1])
                self.real_max += 1
            for i in range(11 - len(self.numbers)):
                self.numbers.append(0)

        connection.close()

    # получить элемент класса по индексу
    def __getitem__(self, i):
        return self.numbers[i]

    # добавить элемент в класс
    def add_record(self, number):
        if self.real_max < self.max:
            self.numbers[self.real_max] = number
            self.real_max += 1
        else:
            for i in range(len(self.numbers) - 1, 0, -1):
                self.numbers[i] = self.numbers[i - 1]
            self.numbers[0] = number

    # вывести все элементы класса в виде текста
    def print_records(self, screen, font):
        for i in range(len(self.numbers) - 1):
            filler_string = str(i + 1) + ". "
            record_surface_index = font.render(filler_string, True, Colors.white)
            screen.blit(record_surface_index, (330, 106 + i * 20, 50, 50))
            filler_string = str(self.numbers[i])
            record_surface_score = font.render(filler_string, True, Colors.white)
            screen.blit(record_surface_score, (370, 106 + i * 20, 50, 50))
        create_table(self.numbers)
        clear_all()

    # сохранить рекорды
    def save_records(self):
        clear_all()
        create_table(self.numbers)
