import pygame
import random
from .base_game import Game, Key, Point2D


CATCHER_SPEED = 1200
BALL_SPEED = 800
BALLS_TO_CATCH = 20


class Catcher(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="CATCHER", **kwargs)
        self.background = pygame.image.load('assets/catcher/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.catcher = pygame.image.load('assets/catcher/treasure_chest.png')
        self.catcher = pygame.transform.scale(self.catcher,
                                              (250, int(250 / self.catcher.get_width() * self.catcher.get_height())))
        self.catcher_loc = Point2D(self.width // 2 - self.catcher.get_width() // 2,
                                   self.height - self.catcher.get_height() - 20)
        self.ball = pygame.image.load('assets/catcher/coin.png')
        self.ball = pygame.transform.scale(self.ball, (self.ball.get_width() // 2, self.ball.get_height() // 2))
        self.ball_loc = None
        self.direction = None  # 1 - left, 2 - right
        self.balls_caught = 0

    def render(self):
        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.catcher, self.catcher_loc)
        if self.ball_loc is not None:
            self.window_surface.blit(self.ball, self.ball_loc)

        self.show_win_percentage(self.balls_caught / BALLS_TO_CATCH)

    def interactive_strategy(self):
        def action(catcher_left, catcher_right, ball_left, ball_right):
            if Key.ARROW_LEFT.value in self.pressed_keys:
                return 1
            if Key.ARROW_RIGHT.value in self.pressed_keys:
                return 2

        return action

    def ingest_strategy(self, direction):
        self.direction = direction

    def get_strategy_parameters(self):
        return [
            self.catcher_loc.x,
            self.catcher_loc.x + self.catcher.get_width(),
            self.ball_loc.x if self.ball_loc is not None else None,
            self.ball_loc.x + self.ball.get_width() if self.ball_loc is not None else None
        ]

    def update_state(self, dt):
        if self.direction == 1:
            self.catcher_loc.x = max(0, self.catcher_loc.x - CATCHER_SPEED * dt)

        if self.direction == 2:
            self.catcher_loc.x = min(self.width - self.catcher.get_width(), self.catcher_loc.x + CATCHER_SPEED * dt)

        if self.ball_loc is None and random.random() <= .05:
            self.ball_loc = Point2D(random.randint(0, self.width - self.ball.get_width()), 0)

        if self.ball_loc is not None:
            self.ball_loc.y += BALL_SPEED * dt

        if self.ball_loc is not None:
            if (self.ball_loc.y > self.catcher_loc.y + self.catcher.get_height() // 3
                    and self.ball_loc.y < self.catcher_loc.y + self.catcher.get_height()
                    and self.ball_loc.x + self.ball.get_width() >= self.catcher_loc.x
                    and self.ball_loc.x <= self.catcher_loc.x + self.catcher.get_width()):
                self.ball_loc = None
                self.balls_caught += 1
            elif self.ball_loc.y > self.height:
                self.lose()

        if self.balls_caught >= BALLS_TO_CATCH:
            self.win()


if __name__ == '__main__':
    Catcher().run()
