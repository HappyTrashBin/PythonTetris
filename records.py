from colors import Colors

class Record:
    def __init__(self):
        self.numbers = [0 for i in range(11)]
        self.max = 10
        self.real_max = 0

    def __getitem__(self, i):
        return self.numbers[i]

    def add_record(self, number):
        if self.real_max < self.max:
            self.numbers[self.real_max] = number
            self.real_max += 1
        else:
            for i in range(len(self.numbers)-1, 0, -1):
                self.numbers[i] = self.numbers[i-1]
            self.numbers[0] = number

    def print_records(self, screen, font):
        for i in range(len(self.numbers) - 1):
            filler_string = str(i) + ". "
            record_surface_index = font.render(filler_string, True, Colors.white)
            screen.blit(record_surface_index, (330, 106 + i * 20, 50, 50))
            filler_string = str(self.numbers[i])
            record_surface_score = font.render(filler_string, True, Colors.white)
            screen.blit(record_surface_score, (350, 106 + i * 20, 50, 50))
