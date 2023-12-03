from grid import Grid
from blocks import *
import random
import pygame
from records import Record


class Game:
    def __init__(self):
        self.grid = Grid()
        self.records = Record()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/block_rotate.mp3")
        self.clear_sound = pygame.mixer.Sound("Sounds/line_clear.mp3")
        self.game_over_sound = pygame.mixer.Sound("Sounds/game_over.mp3")

        pygame.mixer.music.load("Sounds/tetris_sound.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.01)

    def update_score(self, lines_cleared):
        self.score += 100 * lines_cleared

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.score += 1
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.clear_sound.set_volume(0.01)
            self.update_score(rows_cleared)
        if not self.block_fits():
            self.game_over = True
            self.game_over_sound.play()
            self.game_over_sound.set_volume(0.01)

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        if self.score > 0:
            self.records.add_record(self.score)
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()
            self.rotate_sound.set_volume(0.01)

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw_next_block(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 420)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 400)
        else:
            self.next_block.draw(screen, 270, 400)
