import pygame
from colors import Colors


class Grid:
    def __init__(self):
        self.num_rows = 21
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for i in range(self.num_cols)] for j in range(self.num_rows)]
        self.colors = Colors.get_all_colors()

    # проверка на выход за границу игрового поля
    def is_inside(self, row, column):
        if 0 <= row < self.num_rows and 0 <= column < self.num_cols:
            return True
        return False

    # проверка ячейки поля на пустоту
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    # проверка ряда на заполненность
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    # очистка ряда
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    # смещение ряда вниз
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    # очистка более одного ряда
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    # обновить игровое поле
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    # отрисовка игрового поля
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size - 19, self.cell_size - 1,
                                        self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
        pygame.draw.rect(screen, Colors.grey, pygame.Rect(8, -19, self.num_cols * self.cell_size + 6, self.num_rows * self.cell_size + 3), 5, 10)
