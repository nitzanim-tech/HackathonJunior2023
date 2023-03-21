import pygame
from .base_game import Game, Key
import random


GRID_LEFT = 150
GRID_TOP = 50
GRID_SIDE = 500
GRID_CELLS = 25
GRID_CELL_SIDE = GRID_SIDE / GRID_CELLS
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIRECTION_ANGLES = [0, 180, 90, 270]
ACTION_DIRECTIONS = {
    Key.ARROW_LEFT.value: 3,
    Key.ARROW_RIGHT.value: 2,
    Key.ARROW_UP.value: 1,
    Key.ARROW_DOWN.value: 0
}
LENGTH_TO_FINISH = 32


class Snake(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="Snake", framerate=10, **kwargs)
        self.background = pygame.image.load('assets/snake/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        pygame.draw.rect(self.background, pygame.Color("#ceddee"), (GRID_LEFT, GRID_TOP, GRID_SIDE, GRID_SIDE))
        for i in range(GRID_CELLS + 1):
            pos = i * GRID_CELL_SIDE
            pygame.draw.line(self.background, pygame.Color("#6a839b"), (GRID_LEFT, GRID_TOP + pos),
                             (GRID_LEFT + GRID_SIDE, GRID_TOP + pos), width=1)
            pygame.draw.line(self.background, pygame.Color("#6a839b"), (GRID_LEFT + pos, GRID_TOP),
                             (GRID_LEFT + pos, GRID_TOP + GRID_SIDE), width=1)

        self.snake = [
            (0, 0), (0, 1), (0, 2)
        ]

        self.direction_index = 2

        self.snake_rect = pygame.image.load('assets/snake/snake_body.png')
        self.snake_rect = pygame.transform.scale(self.snake_rect, (GRID_CELL_SIDE - 2, GRID_CELL_SIDE - 2))
        self.snake_head = pygame.image.load('assets/snake/snake_head.png')
        self.snake_head = pygame.transform.scale(self.snake_head, (GRID_CELL_SIDE - 2, GRID_CELL_SIDE - 2))
        self.food_pos = None
        self.randomize_food()
        self.food_rect = pygame.image.load('assets/snake/apple.png')
        self.food_rect = pygame.transform.scale(self.food_rect, (GRID_CELL_SIDE - 2, GRID_CELL_SIDE - 2))

    def randomize_food(self):
        self.food_pos = None
        while self.food_pos is None or self.food_pos in self.snake:
            self.food_pos = (random.randint(0, GRID_CELLS - 1), random.randint(0, GRID_CELLS - 1))

    def render(self):
        self.window_surface.blit(self.background, (0, 0))
        for i, (cell_y, cell_x) in enumerate(self.snake):
            surface = self.snake_rect
            if i + 1 == len(self.snake):
                surface = self.snake_head.copy()
                surface = pygame.transform.rotate(surface, DIRECTION_ANGLES[self.direction_index])

            self.window_surface.blit(surface, (
                GRID_LEFT + GRID_CELL_SIDE * cell_x + 1,
                GRID_TOP + GRID_CELL_SIDE * cell_y + 1
            ))

        self.window_surface.blit(self.food_rect, (
            GRID_LEFT + GRID_CELL_SIDE * self.food_pos[1] + 1,
            GRID_TOP + GRID_CELL_SIDE * self.food_pos[0] + 1
        ))

        self.show_win_percentage(len(self.snake) / LENGTH_TO_FINISH)

    def interactive_strategy(self):
        def action(*args):
            return [
                ACTION_DIRECTIONS[k] for k in self.now_pressed_keys if k in ACTION_DIRECTIONS
            ]

        return action

    def ingest_strategy(self, new_direction):
        if new_direction is None:
            return

        if not isinstance(new_direction, list):
            new_direction = [new_direction]

        new_direction = list(filter(
            lambda direction: sum([
                DIRECTIONS[self.direction_index][i] + DIRECTIONS[direction][i] == 0
                for i in range(2)
            ]) != 2,
            new_direction
        ))

        if len(new_direction) == 0:
            return

        self.direction_index = new_direction[0]

    def get_strategy_parameters(self):
        return [
            self.snake, self.food_pos, self.direction_index, GRID_CELLS
        ]

    def update_state(self, dt):
        for i in range(len(self.snake) - 1):
            self.snake[i] = self.snake[i + 1]

        tail = self.snake[0]
        new_head = list(self.snake[-1])
        new_head[0] += DIRECTIONS[self.direction_index][0]
        new_head[1] += DIRECTIONS[self.direction_index][1]
        new_head = tuple(new_head)
        if new_head[0] < 0 or new_head[0] >= GRID_CELLS or new_head[1] < 0 or new_head[1] >= GRID_CELLS or \
                new_head in self.snake[:-1]:
            self.lose()
            return

        self.snake[-1] = new_head
        if self.snake[-1] == self.food_pos:
            self.randomize_food()
            self.snake.insert(0, tail)

        if len(self.snake) >= LENGTH_TO_FINISH:
            self.win()


if __name__ == '__main__':
    Snake().run()
