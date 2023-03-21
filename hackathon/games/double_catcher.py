import pygame
import random
from .base_game import Game, Key, Point2D


CATCHER_SPEED = 1200
BALL_SPEED = 800
BALLS_TO_CATCH = 30


class DoubleCatcher(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="DOUBLE CATCHER", **kwargs)
        self.background = pygame.image.load('assets/catcher/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.catchers = [pygame.image.load('assets/catcher/treasure_chest.png') for _ in range(2)]
        for i in range(len(self.catchers)):
            self.catchers[i] = pygame.transform.scale(self.catchers[i],
                                                      (125,
                                                       int(125 / self.catchers[i].get_width()
                                                           * self.catchers[i].get_height())))
        self.catcher_locs = [Point2D(self.width // 3 - self.catchers[0].get_width() // 2,
                                     self.height - self.catchers[0].get_height() - 20),
                             Point2D(2 * self.width // 3 - self.catchers[0].get_width() // 2,
                                     self.height - self.catchers[0].get_height() - 20)][::-1]
        self.balls = [pygame.image.load('assets/catcher/coin.png') for _ in range(2)]
        for i in range(len(self.balls)):
            self.balls[i] = pygame.transform.scale(
                self.balls[i], (self.balls[i].get_width() // 2, self.balls[i].get_height() // 2)
            )

        self.ball_locs = [None, None]
        self.direction1 = None
        self.direction2 = None
        self.balls_caught = 0

    def render(self):
        self.window_surface.blit(self.background, (0, 0))
        for catcher, catcher_loc in zip(self.catchers, self.catcher_locs):
            self.window_surface.blit(catcher, catcher_loc)

        for ball_loc, ball in zip(self.ball_locs, self.balls):
            if ball_loc is not None:
                self.window_surface.blit(ball, ball_loc)

        self.show_win_percentage(self.balls_caught / BALLS_TO_CATCH)

    def interactive_strategy(self):
        def action(catcher1_left, catcher1_right, catcher2_left, catcher2_right,
                   ball1_left, ball1_right, ball2_left, ball2_right):
            direction1 = None
            direction2 = None
            if Key.ARROW_LEFT.value in self.pressed_keys:
                direction1 = 1
            elif Key.ARROW_RIGHT.value in self.pressed_keys:
                direction1 = 2
            if ord('a') in self.pressed_keys:
                direction2 = 1
            elif ord('d') in self.pressed_keys:
                direction2 = 2

            return direction1, direction2

        return action

    def ingest_strategy(self, directions):
        if directions is not None:
            self.direction1, self.direction2 = directions

    def get_strategy_parameters(self):
        return (sum([[
            catcher_loc.x, catcher_loc.x + catcher.get_width()
        ]
                     for catcher, catcher_loc in zip(self.catchers, self.catcher_locs)], [])
                + sum([[
                    ball_loc.x if ball_loc is not None else None,
                    ball_loc.x + ball.get_width() if ball_loc is not None else None
                ]
                       for ball, ball_loc in zip(self.balls, self.ball_locs)], []))

    def update_state(self, dt):
        if self.direction1 == 1:
            self.catcher_locs[0].x = max(0, self.catcher_locs[0].x - CATCHER_SPEED * dt)

        if self.direction1 == 2:
            self.catcher_locs[0].x = min(self.width - self.catchers[0].get_width(), self.catcher_locs[0].x
                                         + CATCHER_SPEED * dt)

        if self.direction2 == 1:
            self.catcher_locs[1].x = max(0, self.catcher_locs[1].x - CATCHER_SPEED * dt)

        if self.direction2 == 2:
            self.catcher_locs[1].x = min(self.width - self.catchers[1].get_width(), self.catcher_locs[1].x
                                         + CATCHER_SPEED * dt)

        for i in range(len(self.ball_locs)):
            if self.ball_locs[i] is None and random.random() <= .05:
                self.ball_locs[i] = Point2D(random.randint(0, self.width - self.balls[i].get_width()), 0)

            if self.ball_locs[i] is not None:
                self.ball_locs[i].y += BALL_SPEED * dt

            if self.ball_locs[i] is not None:
                caught = False
                for catcher_loc in self.catcher_locs:
                    if (self.ball_locs[i].y > catcher_loc.y
                            and self.ball_locs[i].y < catcher_loc.y + self.catchers[0].get_height()
                            and self.ball_locs[i].x >= catcher_loc.x
                            and self.ball_locs[i].x <= catcher_loc.x + self.catchers[0].get_width()):
                        caught = True
                        break
                if caught:
                    self.ball_locs[i] = None
                    self.balls_caught += 1
                elif self.ball_locs[i].y > self.height:
                    self.lose()

            if self.balls_caught >= BALLS_TO_CATCH:
                self.win()


if __name__ == '__main__':
    DoubleCatcher().run()
