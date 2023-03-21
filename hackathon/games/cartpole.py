import pygame
from .base_game import Game, Key, Point2D
import math
import random


# https://coneural.org/florian/papers/05_cart_pole.pdf

L = 250
M_C = 20
M_P = 5
G = 10
MU_C = .05
MU_P = .000
F = 100000
MAX_THETA = math.pi / 2 * .8
TIME_TO_SURVIVE = 20
HAND_OFFSET = 65


def sign(x):
    if x == 0:
        return 0

    return 2 * int(x > 0) - 1


class CartPole(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="CARTPOLE", **kwargs)
        self.background = pygame.image.load('assets/cartpole/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.cart = pygame.image.load('assets/cartpole/boy.png')
        self.cart_loc = Point2D(self.width // 2 - self.cart.get_width() // 2,
                                self.height - self.cart.get_height() - 70)
        self.move = None  # 1 - left, 2 - right
        self.force = 0
        self.pole_head = pygame.image.load('assets/cartpole/plate.png')
        self.pole_head = pygame.transform.scale(self.pole_head,
                                                (70, 70 / self.pole_head.get_width() * self.pole_head.get_height()))
        self.pole_head_loc = Point2D(self.cart_loc.x + self.cart.get_width() // 2
                                     - self.pole_head.get_width() // 2 + HAND_OFFSET,
                                     self.cart_loc.y - L - self.pole_head.get_height())

        self.theta = (random.random() - .5) / 5
        self.theta_dot = 0
        self.theta_dotdot = 0
        self.x_dot = 0
        self.x_dotdot = 0
        self.n_c = 1

    def render(self):
        pole_base_loc = Point2D(self.cart_loc.x + self.cart.get_width() // 2 + HAND_OFFSET, self.cart_loc.y + 10)
        self.window_surface.blit(self.background, (0, 0))
        pygame.draw.line(self.window_surface, pygame.Color("#111111"),
                         pole_base_loc,
                         (self.pole_head_loc.x + self.pole_head.get_width() // 2,
                          self.pole_head_loc.y + self.pole_head.get_height() // 2))
        self.window_surface.blit(self.cart, self.cart_loc)
        self.window_surface.blit(self.pole_head, self.pole_head_loc)
        self.show_win_percentage(self.running_time / TIME_TO_SURVIVE)

    def interactive_strategy(self):
        def action(*args):
            if Key.ARROW_LEFT.value in self.now_pressed_keys:
                return 1
            elif Key.ARROW_RIGHT.value in self.now_pressed_keys:
                return 2
            return None

        return action

    def ingest_strategy(self, move):
        self.move = move

    def get_strategy_parameters(self):
        return [
            self.cart_loc.x, self.cart_loc.x + self.cart.get_width(), self.x_dot,
            *self.pole_head_loc, L * math.sin(self.theta), L * math.cos(self.theta)
        ]

    def update_state(self, dt):
        dt *= 2
        if self.move == 1:
            self.force = -F
        elif self.move == 2:
            self.force = F
        else:
            self.force = 0

        n_c = (M_C + M_P) * G - M_P * L * (self.theta_dotdot * math.sin(self.theta)
                                           + self.theta_dot ** 2 * math.cos(self.theta))
        self.theta_dotdot = (
                (G * math.sin(self.theta) + math.cos(self.theta)
                 * ((-self.force - M_P * L * self.theta_dot ** 2 * (
                                math.sin(self.theta) + MU_C * sign(n_c * self.x_dot) * math.cos(self.theta)))
                    / (M_P + M_C)
                    + MU_C * G * sign(n_c * self.x_dot))
                 - (MU_P * self.theta_dot) / (M_P * L))
                / (L * (4 / 3 - (M_P * math.cos(self.theta)) / (M_C + M_P) * (
                math.cos(self.theta) - MU_C * sign(n_c * self.x_dot))))
        )

        self.x_dotdot = (
                                self.force + M_P * L * (
                                    self.theta_dot ** 2 * math.sin(self.theta) - self.theta_dotdot * math.cos(
                                self.theta))
                                - MU_C * n_c * sign(n_c * self.x_dot)
                        ) / (M_C + M_P)

        self.theta_dot += self.theta_dotdot * dt
        self.x_dot += self.x_dotdot * dt
        self.theta += self.theta_dot * dt
        self.cart_loc.x += self.x_dot * dt

        self.pole_head_loc.x = (
                self.cart_loc.x + self.cart.get_width() // 2
                - self.pole_head.get_width() // 2 + math.sin(self.theta) * L + HAND_OFFSET
        )
        self.pole_head_loc.y = self.cart_loc.y - math.cos(self.theta) * L

        if abs(self.theta) > MAX_THETA or self.cart_loc.x < 0 or self.cart_loc.x + self.cart.get_width() > self.width:
            self.lose()

        if self.running_time >= TIME_TO_SURVIVE:
            self.win()


if __name__ == '__main__':
    CartPole().run()
