import pygame
from colors import Colors


class Button:
    def __init__(self, x, y, width, height, button_text, change_mode):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alreadyPressed = False
        self.buttonText = button_text

        self.inactive = Colors.silver
        self.active = Colors.grey
        self.pressed = Colors.white

        self.font = pygame.font.Font(None, 40)
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.button_text = self.font.render(self.buttonText, True, Colors.black)
        self.next_page = False
        self.change_mode = change_mode
        self.moving_down_mode = False
        self.color_lock = False

        self.button_sound = pygame.mixer.Sound("Sounds/button.mp3")

    def button_pressed(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if not self.color_lock:
            pygame.draw.rect(screen, self.inactive, self.button_rect, 0, 10)
        else:
            pygame.draw.rect(screen, self.pressed, self.button_rect, 0, 10)
        if self.button_rect.collidepoint(mouse_pos):
            if not self.color_lock:
                pygame.draw.rect(screen, self.active, self.button_rect, 0, 10)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pygame.draw.rect(screen, self.pressed, self.button_rect, 0, 10)
                self.button_sound.play()
                self.button_sound.set_volume(0.01)
                if not self.alreadyPressed:
                    self.next_page = True
                    self.alreadyPressed = True
                    if self.change_mode:
                        self.color_lock = not self.color_lock
                        pygame.draw.rect(screen, self.pressed, self.button_rect, 0, 10)
                        self.moving_down_mode = not self.moving_down_mode
            else:
                self.alreadyPressed = False

        pygame.draw.rect(screen, self.active, self.button_rect, 3, 10)
        screen.blit(self.button_text, self.button_text.get_rect(centerx=self.button_rect.centerx,
                                                                      centery=self.button_rect.centery))
