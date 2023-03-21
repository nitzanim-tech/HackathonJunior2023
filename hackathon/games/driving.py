import pygame
from .base_game import Game, Key, Point2D
import math
import random
from pygame import gfxdraw


GAS_FORCE = 20
FRICTION_MU = 10
H = 16
N = 2000
SIZE = 5000
SENSOR_THETAS = [-math.pi / 4, -math.pi / 8, 0, math.pi / 8, math.pi / 4]
SENSOR_OFFSET = 40
MAX_SENSOR_DISTNACE = 1000
MIN_SENSOR_DISTANCE_FOR_STOPPING = 15
EPSILON = 1e-5
STEER_MAGNITUDE = math.pi / 50
CHECKPOINT_COLLECTION_RADIUS = 200
TIME_TO_FINISH = 30
MAX_SPEED = 2700


def sign(x):
    if x == 0:
        return 0

    return 2 * (int(x > 0) - .5)


def line_intersection(l1_p1, l1_p2, l2_p1, l2_p2):
    x1, y1 = l1_p1
    x2, y2 = l1_p2
    x3, y3 = l2_p1
    x4, y4 = l2_p2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    if (px < min(x1, x2) - EPSILON
            or px > max(x1, x2) + EPSILON
            or px < min(x3, x4) - EPSILON
            or px > max(x3, x4) + EPSILON
            or py < min(y1, y2) - EPSILON
            or py > max(y1, y2) + EPSILON
            or py < min(y3, y4) - EPSILON
            or py > max(y3, y4) + EPSILON
    ):
        return None

    return px, py


def normsq(x, y):
    return x ** 2 + y ** 2


def randomize_track_curves(center_x, center_y, scale, gap):
    rho = [
        10 ** (-.5 - 2 * i / (H - 1)) * random.random()
        for i in range(H)
    ]

    phi = [random.random() * 2 * math.pi for i in range(H)]

    t = [i / (N - 1) * 2 * math.pi for i in range(N)]

    r = [1.2 for i in range(N)]
    for h in range(H):
        for i in range(N):
            r[i] = r[i] + rho[h] * math.sin(h * t[i] + phi[h])

    for i in range(N):
        r[i] *= scale

    x, y = [], []
    xin, yin = [], []
    xout, yout = [], []
    for i in range(N):
        x.append(r[i] * math.cos(t[i]) + center_x)
        y.append(r[i] * math.sin(t[i]) + center_y)
        xin.append((r[i] - gap) * math.cos(t[i]) + center_x)
        yin.append((r[i] - gap) * math.sin(t[i]) + center_y)
        xout.append((r[i] + gap) * math.cos(t[i]) + center_x)
        yout.append((r[i] + gap) * math.sin(t[i]) + center_y)

    for l in [x, y, xin, yin, xout, yout]:
        l.append(l[0])

    return x, y, xin, yin, xout, yout


def create_background():
    background_tile = pygame.image.load('assets/driving/background.png')
    background_tile = pygame.transform.scale(background_tile,
                                             (background_tile.get_width() // 2, background_tile.get_height() // 2))
    background = pygame.Surface((SIZE * 2.5, SIZE * 2.5))
    for row in range(math.ceil(background.get_height() / background_tile.get_height())):
        for col in range(math.ceil(background.get_width() / background_tile.get_width())):
            background.blit(background_tile, (col * background_tile.get_width(), row * background_tile.get_height()))

    return background


class Driving(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="Driving", **kwargs)
        self.x, self.y, self.xin, self.yin, self.xout, self.yout = randomize_track_curves(SIZE, SIZE, SIZE / 2, 120)
        self.background = create_background()
        self.car_loc = Point2D(self.x[0], self.y[0])
        self.car = pygame.image.load('assets/driving/car.png')
        self.car = pygame.transform.scale(self.car, (self.car.get_width() // 1.5, self.car.get_height() // 1.5))
        gfxdraw.filled_polygon(self.background, list(zip(self.xin, self.yin)) + list(zip(self.xout, self.yout))[::-1],
                               pygame.Color('#333344'))
        self.speed = 0
        self.direction = 3 * math.pi / 2
        self.gas = 0
        self.steer = 0
        self.sensor_distances = [MAX_SENSOR_DISTNACE for _ in SENSOR_THETAS]
        self.uncollected_checkpoints = set(zip(self.x, self.y))

    def render(self):
        car = pygame.transform.rotate(self.car.copy(), 180 - self.direction * 180 / math.pi)
        self.window_surface.blit(self.background, (self.width // 2 - self.car_loc.x, self.height // 2 - self.car_loc.y))
        self.window_surface.blit(car, (self.width // 2 - car.get_width() // 2,
                                       self.height // 2 - car.get_height() // 2))
        for theta, sensor_distance in zip(SENSOR_THETAS, self.sensor_distances):
            pygame.draw.line(self.window_surface, pygame.Color("#ffffff"),
                             (self.width // 2 + SENSOR_OFFSET * math.cos(self.direction),
                              self.height // 2 + SENSOR_OFFSET * math.sin(self.direction)),
                             (self.width // 2 + SENSOR_OFFSET * math.cos(self.direction) + sensor_distance * math.cos(self.direction + theta),
                              self.height // 2 + SENSOR_OFFSET * math.sin(self.direction) + sensor_distance * math.sin(self.direction + theta))
                             )

        self.show_win_percentage((1 - len(self.uncollected_checkpoints) / len(self.x)))
        self.show_lose_percentage(1 - self.running_time / TIME_TO_FINISH)

    def interactive_strategy(self):
        def action(*args):
            gas = 0
            steer = 0
            if Key.ARROW_UP.value in self.pressed_keys:
                gas = 1

            if Key.ARROW_LEFT.value in self.pressed_keys:
                steer -= 1
            if Key.ARROW_RIGHT.value in self.pressed_keys:
                steer += 1

            return gas, steer

        return action

    def ingest_strategy(self, actions):
        self.gas, self.steer = actions

    def get_strategy_parameters(self):
        return [
            self.speed, self.sensor_distances
        ]

    def update_state(self, dt):
        self.direction += self.steer * STEER_MAGNITUDE
        self.speed = min(MAX_SPEED, max(self.speed + self.gas * GAS_FORCE - FRICTION_MU, 0))
        if min(self.sensor_distances) < MIN_SENSOR_DISTANCE_FOR_STOPPING:
            self.speed = 0
        self.car_loc.x += self.speed * math.cos(self.direction) * dt
        self.car_loc.y += self.speed * math.sin(self.direction) * dt
        self.sensor_distances = [
            self.calculate_sensor_distance(
                (self.car_loc.x + SENSOR_OFFSET * math.cos(self.direction),
                 self.car_loc.y + SENSOR_OFFSET * math.sin(self.direction)),
                theta
            )
            for theta in SENSOR_THETAS
        ]

        self.uncollected_checkpoints -= {
            checkpoint for checkpoint in self.uncollected_checkpoints
            if normsq(checkpoint[0] - self.car_loc.x, checkpoint[1] - self.car_loc.y)
               <= CHECKPOINT_COLLECTION_RADIUS ** 2
        }

        if len(self.uncollected_checkpoints) == 0:
            self.win()
        elif self.running_time >= TIME_TO_FINISH:
            self.lose()

    def calculate_sensor_distance(self, sensor_origin, theta):
        endpoint = (sensor_origin[0] + MAX_SENSOR_DISTNACE * math.cos(self.direction + theta),
                    sensor_origin[1] + MAX_SENSOR_DISTNACE * math.sin(self.direction + theta))
        for i in range(len(self.xin) - 1):
            p1 = (self.xin[i], self.yin[i])
            p2 = (self.xin[i + 1], self.yin[i + 1])
            intersection = line_intersection(sensor_origin, endpoint, p1, p2)
            if intersection is not None:
                endpoint = intersection

        for i in range(len(self.xout) - 1):
            p1 = (self.xout[i], self.yout[i])
            p2 = (self.xout[i + 1], self.yout[i + 1])
            intersection = line_intersection(sensor_origin, endpoint, p1, p2)
            if intersection is not None:
                endpoint = intersection

        return math.sqrt(math.pow(endpoint[0] - sensor_origin[0], 2)
                         + math.pow(endpoint[1] - sensor_origin[1], 2))


if __name__ == '__main__':
    Driving().run()
