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

        self.font = pygame.font.Font('BrassMono.ttf', 40)

        self.value = 0.05
        self.slider_space = pygame.Rect(self.x,
                                        self.y,
                                        self.width,
                                        self.height)
        self.bar_rect = pygame.Rect(self.x + self.width / 10,
                                    self.y + self.height * 3 / 5,
                                    self.width * 0.8,
                                    self.height / 10)
        self.moving_part_rect = pygame.Rect(self.x + self.width / 10 + self.value*self.width * 0.8,
                                            self.y + self.height * 1 / 2,
                                            self.width * 0.08,
                                            self.height * 3 / 10)
        self.hitbox_rect = pygame.Rect(self.x + self.width / 10 + self.width * 0.04,
                                       self.y + self.height * 1 / 2,
                                       self.width * 0.8 - self.width * 0.04,
                                       self.height * 3 / 10)

        self.text = self.font.render(self.slider_text, True, Colors.black)

        self.button_sound = pygame.mixer.Sound("Sounds/button.mp3")
        self.button_volume = 0.05

        self.mouse_flag = False

    # нарисовать ползунок, проверить на перемещение
    def draw_slider(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect, 0, 10)
        if self.hitbox_rect.collidepoint(mouse_pos):
            if self.x + self.width / 10 <= self.moving_part_rect.x <= self.x + self.width * 9 / 10 - self.width * 0.08:
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.moving_part_rect = pygame.Rect(mouse_pos[0] - self.width * 0.04,
                                                        self.y + self.height * 1 / 2,
                                                        self.width * 0.08,
                                                        self.height * 3 / 10)
                    pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect, 0, 10)

                    if self.moving_part_rect.x < self.x:
                        self.moving_part_rect.x = self.x
                    elif self.moving_part_rect.x > self.x + self.width * 9 / 10 - self.width * 0.08:
                        self.moving_part_rect.x = self.x + self.width * 9 / 10 - self.width * 0.08

                    self.value = round(((self.moving_part_rect.x - self.x - self.width / 10 + self.width * 0.08 * (
                                self.moving_part_rect.x - self.x - self.width / 10) / (
                                                     self.width * 8 / 10 - self.width * 0.08)) / self.bar_rect.width),
                                       2)
                    self.button_sound.play()

        pygame.draw.rect(screen, self.background_color, self.slider_space, 0, 10)
        pygame.draw.rect(screen, self.bar_color, self.slider_space, 3, 10)
        pygame.draw.rect(screen, self.bar_color, self.bar_rect, 0, 10)
        pygame.draw.rect(screen, self.moving_part_color, self.moving_part_rect)
        screen.blit(self.text, self.text.get_rect(centerx=self.slider_space.centerx,
                                                  centery=self.slider_space.centery - 25))

    # установить громкость звука ползунка
    def set_slider_sound(self, volume):
        self.button_volume = volume
        self.button_sound.set_volume(self.button_volume)
