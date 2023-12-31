import sys
import pygame

from game import Game
from colors import Colors
from button import Button
from drawing import Drawing
from slider import Slider

# pygame инициализация
pygame.init()

# текстовые элементы, фигуры и оформление главного меню
title_font = pygame.font.Font('BrassMono.ttf', 40)
lower_font = pygame.font.Font('BrassMono.ttf', 20)
score_text = title_font.render("Score", True, Colors.black)
next_text = title_font.render("Next", True, Colors.black)
moving_modes_first = lower_font.render("off - block moves down each pressing", True, Colors.black)
moving_modes_second = lower_font.render("on - block moves down while pressing", True, Colors.black)
score_rect = pygame.Rect(320, 45, 170, 50)
record_rect = pygame.Rect(320, 100, 170, 210)
next_rect = pygame.Rect(320, 345, 170, 180)
tetris = Drawing()

# создание экрана программы
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")
pygame.display.set_icon(pygame.image.load('tetris.png'))

# таймер
clock = pygame.time.Clock()

# вызов основного класса Game
game = Game()

# создание отдельного события для расчёта сложности, переменной времени и скорости пассивного движения блоков
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

# пауза, сложность, режим нажатия, кнопки и ползунки
pause = True
difficulty = 0
moving_down_mode = False
current_time = 0
button_main = Button(150, 455, 200, 70, 'Play', False)
button_next = Button(50, 20, 400, 70, 'Begin game', False)
button_change_mode = Button(50, 100, 400, 70, 'Change button mode', True)
difficulty_slider = Slider(125, 220, 250, 100, 'Difficulty')
main_sound_slider = Slider(125, 330, 250, 100, 'Main sound')
other_sound_slider = Slider(125, 440, 250, 100, 'Other sound')

# игровой цикл
while not button_main.next_page and not button_next.next_page:
    # главное окно
    for event in pygame.event.get():
        # закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # оформление
    screen.fill(Colors.white)
    tetris.draw_background(screen, 21, 18)
    tetris.draw_main(screen)

    # кнопка перехода на экран настроек
    button_main.button_pressed(screen)
    tetris.draw_title(screen)

    pygame.display.update()
    clock.tick(30)
while button_main.next_page and not button_next.next_page:
    # окно настроек
    for event in pygame.event.get():
        # закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # оформление
    screen.fill(Colors.silver)

    # кнопка перехода на игровое окно
    button_next.button_pressed(screen)

    # кнопка смены режима работы смещения блока вниз (выкл - раз за нажатие, вкл - до нижней границы при зажатии)
    button_change_mode.button_pressed(screen)
    screen.blit(moving_modes_first, moving_modes_first.get_rect(centerx=button_change_mode.button_rect.centerx,
                                                                centery=button_change_mode.button_rect.centery + 50
                                                                )
                )
    screen.blit(moving_modes_second, moving_modes_second.get_rect(centerx=button_change_mode.button_rect.centerx,
                                                                  centery=button_change_mode.button_rect.centery+70
                                                                  )
                )
    # ползунок определения сложности
    difficulty_slider.draw_slider(screen)
    # ползунок определения основного звука
    main_sound_slider.draw_slider(screen)
    # ползунок определения неосновного звука
    other_sound_slider.draw_slider(screen)

    # изменение звука в зависимости от значения ползунков
    game.set_main_volume(main_sound_slider.value)
    game.set_other_volume(other_sound_slider.value)
    button_next.set_button_sound(other_sound_slider.value)
    button_change_mode.set_button_sound(other_sound_slider.value)
    difficulty_slider.set_slider_sound(other_sound_slider.value)
    main_sound_slider.set_slider_sound(other_sound_slider.value)
    other_sound_slider.set_slider_sound(other_sound_slider.value)

    pygame.display.update()
    clock.tick(60)
while button_main.next_page and button_next.next_page:
    # игровое окно
    for event in pygame.event.get():

        # закрытие окна
        if event.type == pygame.QUIT:
            game.records.save_records()
            pygame.quit()
            sys.exit()

        # до тех пор, пока не нажата любая клавиша, игра стоит на паузе
        if event.type == pygame.KEYDOWN:
            pause = False

            # конец игры
            if game.game_over:
                game.game_over = False
                game.reset()

            # движение влево, вправо, вниз раз за нажатие
            if event.key == pygame.K_LEFT and not game.game_over and not pause:
                game.move_left()
            if event.key == pygame.K_RIGHT and not game.game_over and not pause:
                game.move_right()
            if (event.key == pygame.K_DOWN and not game.game_over and not pause and
                    not button_change_mode.moving_down_mode):
                game.move_down()

            # поворот блока
            if event.key == pygame.K_UP and not game.game_over and not pause:
                game.rotate()

            # запуск игровой сессии заново
            if event.key == pygame.K_SPACE:
                game.reset()

            # пауза в процессе игры
            if event.key == pygame.K_ESCAPE:
                pause = True

        # счётчик сложности, скорости пассивного движения блоков и изменения временной переменной
        if event.type == GAME_UPDATE and not game.game_over and not pause:
            game.move_down()
            current_time += 1
            if difficulty <= 450:
                difficulty += 1 + difficulty_slider.value * 4
                pygame.time.set_timer(GAME_UPDATE, 550 - round(difficulty))

    # движение вниз при зажатии
    if button_change_mode.moving_down_mode:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and not game.game_over and not pause:
            game.move_down()

    # заполнение фона
    screen.fill(Colors.black)
    tetris.draw_moving_background(screen, 21, 18, current_time)

    # отображение текущего счёта
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    screen.blit(score_text, score_text.get_rect(centerx=score_rect.centerx,
                                                centery=score_rect.centery - 40))

    pygame.draw.rect(screen, Colors.black, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.grey, score_rect, 5, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery + 2))

    # отображение прошлых рекордов
    pygame.draw.rect(screen, Colors.black, record_rect, 0, 10)
    pygame.draw.rect(screen, Colors.grey, record_rect, 5, 10)
    game.records.print_records(screen, lower_font)

    # место для отображения следующей фигуры
    screen.blit(next_text, next_text.get_rect(centerx=next_rect.centerx,
                                              centery=next_rect.centery - 105))
    pygame.draw.rect(screen, Colors.black, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.grey, next_rect, 5, 10)

    # отрисовка текущего блока на игровом поле и следующего блока в соответствующем месте
    game.draw_blocks(screen)

    # конец игры
    if game.game_over:
        tetris.game_over(screen)

    # пауза
    if pause:
        tetris.pause_screen(screen)

    # обновление экрана и частота обновления экрана
    pygame.display.update()
    clock.tick(60)
