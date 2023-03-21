import pygame
from .base_game import Game, Key, Point2D
import random


G = 1000
FORCE = -45000
PIPE_SPEED = 150
PIPE_GAP_HEIGHT_RATIO = .4
TIME_TO_SURVIVE = 25


class FlappyBird(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="Flappy Bird", **kwargs)
        self.background = pygame.image.load('assets/flappy_bird/background.png')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.bird_loc = Point2D(200, 200)
        self.y_dot = -500
        self.bird = pygame.image.load('assets/flappy_bird/bat.png')
        self.bird = pygame.transform.scale(self.bird,
                                           (70 / self.bird.get_height() * self.bird.get_width(), 70))
        self.bird_flap = pygame.image.load('assets/flappy_bird/bat_flap.png')
        self.bird_flap = pygame.transform.scale(self.bird_flap,
                                                (70 / self.bird_flap.get_height() * self.bird_flap.get_width(), 70))
        self.flap = False
        self.pipes = []
        self.pipe = pygame.image.load('assets/flappy_bird/pipe.png')

        self.background_offset_x = 0
        self.time_since_last_flap = 0

    def render(self):
        self.window_surface.blit(self.background, (self.background_offset_x, 0))
        self.window_surface.blit(self.background, (self.background_offset_x
                                                   + self.background.get_width(), 0))
        bird_surface = self.bird
        if self.time_since_last_flap < .3:
            bird_surface = self.bird_flap

        self.window_surface.blit(bird_surface, (self.bird_loc[0] - self.bird.get_width() // 2,
                                                self.bird_loc[1] - self.bird.get_height() // 2))
        for pipe_x, pipe_top_y in self.pipes:
            self.window_surface.blit(pygame.transform.flip(self.pipe, False, True),
                                     (pipe_x - self.pipe.get_width() // 2,
                                      pipe_top_y - self.pipe.get_height()))
            self.window_surface.blit(self.pipe, (pipe_x - self.pipe.get_width() // 2,
                                                 pipe_top_y + PIPE_GAP_HEIGHT_RATIO * self.height))

        self.show_win_percentage(self.running_time / TIME_TO_SURVIVE)

    def interactive_strategy(self):
        def action(*args):
            if ord(' ') in self.now_pressed_keys:
                return 1

            return None

        return action

    def ingest_strategy(self, flap):
        self.flap = flap == 1

    def get_strategy_parameters(self):
        return [
            self.bird_loc.y, self.y_dot,
            [
                (pipe_x - self.bird_loc.x - self.bird.get_width() // 2 - self.pipe.get_width() // 2,
                 pipe_top_y + self.bird.get_height() // 2,
                 pipe_top_y + PIPE_GAP_HEIGHT_RATIO * self.height - self.bird.get_height() // 2)
                for pipe_x, pipe_top_y in self.pipes
                if pipe_x + self.pipe.get_width() // 2 > self.bird_loc.x - self.bird.get_width() // 2
            ]
        ]

    def update_state(self, dt):
        self.time_since_last_flap += dt
        if self.flap:
            self.time_since_last_flap = 0

        self.y_dot += dt * G + dt * self.flap * FORCE
        self.bird_loc.y += dt * self.y_dot
        self.flap = False
        if self.bird_loc.y - self.bird.get_height() // 2 < 0 or \
                self.bird_loc.y + self.bird.get_height() // 2 > self.height:
            self.lose()

        i = 0
        while i < len(self.pipes):
            self.pipes[i][0] -= PIPE_SPEED * dt
            if self.pipes[i][0] < 0:
                del self.pipes[i]
            else:
                i += 1

        self.background_offset_x -= PIPE_SPEED * dt
        if self.background_offset_x <= -self.background.get_width():
            self.background_offset_x = 0

        if (len(self.pipes) == 0 or self.pipes[-1][0] < .6 * self.width) and random.random() <= .03:
            self.pipes.append([
                self.width, random.random() * .3 * self.height
            ])

        for pipe_x, pipe_top_y in self.pipes:
            if abs(pipe_x - self.bird_loc.x) <= self.pipe.get_width() // 2 + self.bird.get_width() // 2 and \
                    (self.bird_loc.y - self.bird.get_height() // 2 < pipe_top_y
                     or self.bird_loc.y + self.bird.get_height() // 2 >
                     pipe_top_y + PIPE_GAP_HEIGHT_RATIO * self.height):
                self.lose()
                break

        if self.running_time >= TIME_TO_SURVIVE:
            self.win()


if __name__ == '__main__':
    FlappyBird().run()
