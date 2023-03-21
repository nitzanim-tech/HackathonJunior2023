import pygame
from .base_game import Game, Key, Point2D
import math


START_X = 330
RADIUS = 20
FORCE = 70
FRICTION_MU = 60
G = 200
FLAG_X = 740
TIME_TO_FINISH = 32


def sign(x):
    if x == 0:
        return 0

    return 2 * (int(x > 0) - .5)


def ground(x):
    x = (x - 340) / 300
    return 500 + 200 * (x ** 3 - 2 * x ** 2)


def ground_dot(x):
    x = (x - 340) / 300
    return 200 * (3 * x ** 2 - 4 * x) / 300


def draw_ground(surface):
    y_prev = int(ground(0))
    for x in range(1, surface.get_width() + 1):
        y = int(ground(x))
        pygame.draw.line(surface, pygame.Color('#ffffff'), (x - 1, y_prev), (x, y))
        y_prev = y


class MountainCar(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="MountainCar", **kwargs)
        self.background = pygame.image.load('assets/mountaincar/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.car_loc = Point2D(START_X, ground(START_X))
        self.x_dot = 0
        self.direction = None  # 1 for left, 2 for right
        self.flag = pygame.image.load('assets/mountaincar/flag.png')
        self.flag = pygame.transform.scale(self.flag, (self.flag.get_width() // 1.5, self.flag.get_height() // 1.5))
        self.car = pygame.image.load('assets/mountaincar/car.png')
        self.car = pygame.transform.scale(self.car, (self.car.get_width() // 1.5, self.car.get_height() // 1.5))
        self.x_dotdot = 0

    def render(self):
        tangent_slope = ground_dot(self.car_loc.x)
        normal_angle = -.5 * math.pi
        if tangent_slope != 0:
            normal_angle = math.atan(-1 / tangent_slope)

        if normal_angle > 0:
            normal_angle += math.pi

        offset_x = math.cos(normal_angle) * self.car.get_height() / 2
        offset_y = math.sin(normal_angle) * self.car.get_height() / 2

        self.window_surface.blit(self.background, (0, 0))
        car = pygame.transform.rotate(self.car, -math.atan(tangent_slope) * 180 / math.pi)
        self.window_surface.blit(car, (self.car_loc.x - car.get_width() // 2 + offset_x,
                                       self.car_loc.y - car.get_height() // 2 + offset_y))

        self.window_surface.blit(self.flag, (FLAG_X,
                                             ground(FLAG_X) - self.flag.get_height()))

        self.show_lose_percentage(1 - self.running_time / TIME_TO_FINISH)

    def interactive_strategy(self):
        def action(*args):
            if Key.ARROW_LEFT.value in self.pressed_keys:
                return 1
            elif Key.ARROW_RIGHT.value in self.pressed_keys:
                return 2
            return None

        return action

    def ingest_strategy(self, direction):
        self.direction = direction

    def get_strategy_parameters(self):
        return [
            self.x_dot, self.x_dotdot
        ]

    def update_state(self, dt):
        dt *= 2
        direction_sign = -1 if self.direction == 1 else 1 if self.direction == 2 else 0
        self.x_dotdot = G * ground_dot(self.car_loc.x) - sign(self.x_dot) * FRICTION_MU + direction_sign * FORCE
        self.x_dot += self.x_dotdot * dt
        self.car_loc.x += self.x_dot * dt
        self.car_loc.y = ground(self.car_loc.x)
        if self.car_loc.x >= FLAG_X:
            self.win()

        if self.running_time >= TIME_TO_FINISH:
            self.lose()


if __name__ == '__main__':
    MountainCar().run()
