from colors import Colors
import pygame
from grid import Grid
from game import Game
import random


class Drawing:
    def __init__(self):
        self.main_title_font = pygame.font.Font('BrassMono.ttf', 100)
        self.lower_title_font = pygame.font.Font('BrassMono.ttf', 40)
        self.letters = ['T', 'E', 'T', 'R', 'I', 'S']
        self.game = Game()
        self.x_position = 0
        self.cell_size = Grid().cell_size
        self.colors = Colors.get_all_colors()
        self.game_over_text = self.lower_title_font.render("GAME OVER", True, Colors.white)
        self.pause_text = self.lower_title_font.render("PAUSE", True, Colors.white)

    # нарисовать заголовок
    def draw_title(self, screen):
        tetris_rect = pygame.Rect(100, 65, 300, 100)
        pygame.draw.rect(screen, Colors.black, tetris_rect, 0, 15)
        pygame.draw.rect(screen, Colors.white, tetris_rect, 3, 15)
        for i in range(len(self.letters)):
            tetris_surface = self.main_title_font.render(self.letters[i], True, self.colors[i+1])
            screen.blit(tetris_surface,
                        tetris_surface.get_rect(centerx=tetris_rect.centerx - 122 + 49*i,
                                                centery=tetris_rect.centery + 7))

    # нарисовать фон в виде игрового поля
    def draw_background(self, screen, rows, columns):
        for row in range(rows):
            for column in range(columns):
                cell_rect = pygame.Rect(column * self.cell_size - 5, row * self.cell_size - 5, self.cell_size - 1,
                                        self.cell_size - 1)
                pygame.draw.rect(screen, Colors.black, cell_rect)

    # нарисовать движущиеся блоки на фоне
    def draw_main(self, screen):
        if self.game.next:
            self.x_position = random.randint(-3, 9) * 30 + 25
            self.game.rotate = True
            self.game.next = False
        self.game.current_block.draw(screen, self.x_position, -65)
        self.game.move_down_in_main(screen)
        self.game.rotate_main()
        self.game.rotate = False

    def game_over(self, screen):
        x, y = pygame.display.get_surface().get_size()
        w, h = 250, 100
        tetris_rect = pygame.Rect((x-w)/2, (y-h)/2, w, h)
        pygame.draw.rect(screen, Colors.black, tetris_rect, 0, 15)
        pygame.draw.rect(screen, Colors.grey, tetris_rect, 3, 15)
        screen.blit(self.game_over_text, self.game_over_text.get_rect(centerx=tetris_rect.centerx,
                                                                      centery=tetris_rect.centery + 2))

    def pause_screen(self, screen):
        x, y = pygame.display.get_surface().get_size()
        w, h = 250, 100
        tetris_rect = pygame.Rect((x - w) / 2, (y - h) / 2, w, h)
        pygame.draw.rect(screen, Colors.black, tetris_rect, 0, 15)
        pygame.draw.rect(screen, Colors.grey, tetris_rect, 3, 15)
        screen.blit(self.pause_text,
                    self.pause_text.get_rect(centerx=tetris_rect.centerx, centery=tetris_rect.centery + 2))
