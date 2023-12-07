import pygame
from colors import Colors


class Slider:
    def __init__(self, x, y, width, height, slider_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.slider_text = slider_text

        self.bar_color = Colors.grey
        self.moving_part_color = Colors.blue
        self.background_color = Colors.silver

        self.font = pygame.font.Font(None, 40)
        self.slider_space = pygame.Rect(self.x,
                                        self.y,
                                        self.width,
                                        self.height)
        self.bar_rect = pygame.Rect(self.x + self.width/10,
                                    self.y + self.height*3/5,
                                    self.width*0.8,
                                    self.height/10)
        self.moving_part_rect = pygame.Rect(self.x + self.width/10,
                                            self.y + self.height*1/2,
                                            self.width*0.08,
                                            self.height*3/10)

        self.text = self.font.render(self.slider_text, True, Colors.black)

        self.difficulty = 0

    def slider_moved(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect, 0, 10)
        if self.bar_rect.collidepoint(mouse_pos):
            if self.x + self.width / 10 <= self.moving_part_rect.x <= self.x + self.width * 9 / 10 - self.width * 0.08:
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.moving_part_rect = pygame.Rect(mouse_pos[0] - self.width * 0.04,
                                                        self.y + self.height*1/2,
                                                        self.width * 0.08,
                                                        self.height * 3 / 10)
                    pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect, 0, 10)
                    if not self.x + self.width / 10 <= self.moving_part_rect.x:
                        self.moving_part_rect.x = self.x + self.width / 10
                    elif not self.moving_part_rect.x <= self.x + self.width * 9 / 10 - self.width * 0.08:
                        self.moving_part_rect.x = self.x + self.width * 9 / 10 - self.width * 0.08
                    self.difficulty = round(((self.moving_part_rect.x - self.x) / 100) / (self.bar_rect.width / 100), 2)
                    if self.difficulty > 1:
                        self.difficulty = 1

        pygame.draw.rect(screen, self.background_color, self.slider_space, 0, 10)
        pygame.draw.rect(screen, self.bar_color, self.slider_space, 3, 10)
        pygame.draw.rect(screen, self.bar_color, self.bar_rect, 0, 10)
        pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect)
        screen.blit(self.text, self.text.get_rect(centerx=self.slider_space.centerx,
                                                  centery=self.slider_space.centery - 25))

