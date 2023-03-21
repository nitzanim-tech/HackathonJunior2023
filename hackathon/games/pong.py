import pygame
import random
import math
from .base_game import Game, Key, Point2D


PONG_SPEED = 800
BALL_SPEED = 1500
MARGIN = 25
ANGLE_MARGIN = math.pi / 6
PINGS_TO_FINISH = 30


def sign(x):
    return 2 * int(x > 0) - 1


class Pong(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="PONG", **kwargs)
        self.background = pygame.image.load('assets/pong/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.pong = pygame.image.load('assets/pong/pong.png')
        self.pong = pygame.transform.scale(self.pong,
                                           (150 / self.pong.get_height() * self.pong.get_width(),
                                            150))
        self.pong_loc = Point2D(20, self.height // 2)
        self.mirror = pygame.Surface((25, self.height))
        self.mirror.fill(pygame.Color("#e0b867"))
        self.mirror_loc = Point2D(self.width - self.mirror.get_width(), 0)
        self.wall = pygame.Surface((self.width, MARGIN))
        self.wall.fill(pygame.Color("#e0b867"))
        self.ball = pygame.image.load('assets/pong/pool_ball.png')
        self.ball = pygame.transform.scale(self.ball, (60, 60))
        self.ball_loc = Point2D(self.width // 4, self.height // 2)
        self.ball_angle = self.randomize_angle()

        self.direction = None  # 1 for up, 2 for down
        self.pings = 0

    def randomize_angle(self):
        max_angle = math.atan2(self.height // 2, self.width // 2)
        min_angle = -max_angle

        return random.random() * (max_angle - min_angle) + min_angle

    def render(self):
        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.pong, self.pong_loc)
        self.window_surface.blit(self.ball, self.ball_loc)
        self.show_win_percentage(self.pings / PINGS_TO_FINISH)

    def interactive_strategy(self):
        def action(*args):
            if Key.ARROW_UP.value in self.pressed_keys:
                return 1
            elif Key.ARROW_DOWN.value in self.pressed_keys:
                return 2
            return None

        return action

    def ingest_strategy(self, direction):
        self.direction = direction

    def get_strategy_parameters(self):
        return [
            self.pong_loc.x + self.pong.get_width(),
            self.pong_loc.y, self.pong_loc.y + self.pong.get_height(),
            self.width - MARGIN, MARGIN, self.height - MARGIN,
            self.ball_loc.x, self.ball_loc.y, math.cos(self.ball_angle), math.sin(self.ball_angle)
        ]

    def update_state(self, dt):
        if self.direction == 1:
            self.pong_loc.y = max(MARGIN, self.pong_loc.y - PONG_SPEED * dt)
        elif self.direction == 2:
            self.pong_loc.y = min(self.height - self.pong.get_height() - MARGIN, self.pong_loc.y + PONG_SPEED * dt)

        if ((self.ball_loc.x + self.ball.get_width() >= self.width - MARGIN
                and math.cos(self.ball_angle) > 0)
            or ((self.ball_loc.x <= self.pong_loc.x + self.pong.get_width()
                and self.ball_loc.x >= self.pong_loc.x
                or self.ball_loc.x + self.ball.get_width() <= self.pong_loc.x + self.pong.get_width()
                and self.ball_loc.x + self.ball.get_width() >= self.pong_loc.x)
                and self.ball_loc.y >= self.pong_loc.y
                and self.ball_loc.y + self.ball.get_height() // 2 <= self.pong_loc.y + self.pong.get_height()
                and math.cos(self.ball_angle) < 0)):
            if math.cos(self.ball_angle) < 0:
                self.pings += 1

            self.ball_angle = (sign(self.ball_angle) * (math.pi - abs(self.ball_angle))
                               + (2 * random.random() - 1) * math.pi / 10)
        elif ((self.ball_loc.y <= MARGIN or self.ball_loc.y + self.ball.get_height() >= self.height - MARGIN)
                and sign(math.sin(self.ball_angle)) == sign(self.ball_loc.y - self.height // 2)):
            self.ball_angle *= -1

        angle_sign = sign(self.ball_angle)
        self.ball_angle = abs(self.ball_angle)
        if self.ball_angle > math.pi / 2 - ANGLE_MARGIN and self.ball_angle <= math.pi / 2:
            self.ball_angle = math.pi / 2 - ANGLE_MARGIN
        elif self.ball_angle >= math.pi / 2 and self.ball_angle < math.pi / 2 + ANGLE_MARGIN:
            self.ball_angle = math.pi / 2 + ANGLE_MARGIN

        self.ball_angle *= angle_sign

        self.ball_loc.x += math.cos(self.ball_angle) * BALL_SPEED * dt
        self.ball_loc.y += math.sin(self.ball_angle) * BALL_SPEED * dt

        self.ball_loc.x = min(self.ball_loc.x, self.width - MARGIN)
        self.ball_loc.y = max(MARGIN, min(self.ball_loc.y, self.height - MARGIN))

        if self.ball_loc.x + self.ball.get_width() < 0:
            self.lose()

        if self.pings >= PINGS_TO_FINISH:
            self.win()


if __name__ == '__main__':
    Pong().run()
