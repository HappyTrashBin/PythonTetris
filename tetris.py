import sys
import pygame
from game import Game
from colors import Colors
from button import Button
from drawing import Tetris

# pygame инициализация
pygame.init()

# текстовые элементы и фигуры
title_font = pygame.font.Font(None, 40)
lower_font = pygame.font.Font(None, 25)
score_text = title_font.render("Score", True, Colors.black)
next_text = title_font.render("Next", True, Colors.black)
game_over_text = title_font.render("GAME OVER", True, Colors.black)
moving_modes_first = lower_font.render("turn off - block moves down ones per pressing", True, Colors.black)
moving_modes_second = lower_font.render("turn on - block moves down while pressing", True, Colors.black)
difficulty = 0
tetris = Tetris()

score_rect = pygame.Rect(320, 45, 170, 50)
record_rect = pygame.Rect(320, 100, 170, 210)
next_rect = pygame.Rect(320, 345, 170, 180)

# создание экрана программы
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

# таймер
clock = pygame.time.Clock()

# вызов основного класса Game
game = Game()

# создание отдельного события для рассчёта сложности и скорости пассивного движения блоков
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# пауза, сложность, режим нажатия, кнопки
pause = True
difficulty = 0
moving_down_mode = False
button_main = Button(150, 455, 200, 70, 'Play', False)
button_next = Button(150, 20, 200, 70, 'Begin game', False)
button_change_mode = Button(75, 100, 350, 70, 'Change button mode', True)

# игровой цикл
while True:
    # главное окно
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(Colors.white)
    tetris.draw_background(screen, 21, 18)

    tetris.draw_main(screen)

    # кнопка перехода на экран настроек
    button_main.button_pressed(screen)
    tetris.draw_title(screen)
    pygame.display.update()
    clock.tick(15)
    while button_main.next_page:
        # окно настроек
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(Colors.silver)
        # кнопка перехода на игровое окно
        button_next.button_pressed(screen)
        # кнопка смены режима работы смещения блока вниз (выкл - раз за нажатие, вкл - до нижней границы при зажатии)
        button_change_mode.button_pressed(screen)
        screen.blit(moving_modes_first, moving_modes_first.get_rect(centerx=button_change_mode.button_rect.centerx,
                                                                      centery=button_change_mode.button_rect.centery + 45))
        screen.blit(moving_modes_second, moving_modes_second.get_rect(centerx=button_change_mode.button_rect.centerx,
                                                                      centery=button_change_mode.button_rect.centery + 65))
        pygame.display.update()
        clock.tick(15)
        while button_next.next_page:
            for event in pygame.event.get():
                # закрытие окна
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # до тех пор, пока не нажата любая клавиша, игра стоит на паузе
                if event.type == pygame.KEYDOWN:
                    pause = False
                    # конец игры
                    if game.game_over:
                        game.game_over = False
                        game.reset()
                        pause = True
                    # движение влево, вправо, вниз раз за нажатие
                    if event.key == pygame.K_LEFT and not game.game_over and not pause:
                        game.move_left()
                    if event.key == pygame.K_RIGHT and not game.game_over and not pause:
                        game.move_right()
                    if event.key == pygame.K_DOWN and not game.game_over and not pause and not button_change_mode.moving_down_mode:
                        game.move_down()
                    # поворот блока
                    if event.key == pygame.K_UP and not game.game_over and not pause:
                        game.rotate()
                    # запуск игровой сессии заного
                    if event.key == pygame.K_SPACE:
                        game.reset()
                    # счётчик сложности и скорости пассивного движения блоков
                if event.type == GAME_UPDATE and not game.game_over and not pause:
                    game.move_down()
                    if difficulty < 125:
                        difficulty += 0.1
                        pygame.time.set_timer(GAME_UPDATE, 200 - round(difficulty))
            # движение вниз при зажатии
            if button_change_mode.moving_down_mode:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN] and not game.game_over and not pause:
                    game.move_down()

            # заполнение фона
            screen.fill(Colors.silver)

            # отображение текущего счёта
            score_value_surface = title_font.render(str(game.score), True, Colors.white)
            screen.blit(score_text, (365, 15))
            pygame.draw.rect(screen, Colors.black, score_rect, 0, 10)
            pygame.draw.rect(screen, Colors.grey, score_rect, 5, 10)
            screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))

            # отображение прошлых рекордов
            pygame.draw.rect(screen, Colors.black, record_rect, 0, 10)
            pygame.draw.rect(screen, Colors.grey, record_rect, 5, 10)
            game.records.print_records(screen, lower_font)

            # место для отображения следующей фигуры
            screen.blit(next_text, (375, 315))
            pygame.draw.rect(screen, Colors.black, next_rect, 0, 10)
            pygame.draw.rect(screen, Colors.grey, next_rect, 5, 10)

            # отрисовка текущего блока на игровом поле и следующего блока в соответствующем месте
            game.draw_blocks(screen)

            # конец игры
            if game.game_over:
                screen.blit(game_over_text, (320, 550))

            # обновление экрана и частота обновления экрана
            pygame.display.update()
            clock.tick(15)
