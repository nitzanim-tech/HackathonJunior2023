import pygame
from enum import Enum
from time import sleep
import json
import hashlib
import base64
from datetime import datetime


def sha256_encode(text):
    m = hashlib.sha256()
    m.update(text)
    return m.hexdigest()


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y

        raise ValueError("Point2D only has two coordinates")

    def __len__(self):
        return 2

    def __iter__(self):
        yield from [self[i] for i in range(len(self))]


class Key(Enum):
    ARROW_LEFT = 1073741904
    ARROW_RIGHT = 1073741903
    ARROW_UP = 1073741906
    ARROW_DOWN = 1073741905
    SPACE = 32


class Colors:
    red = pygame.Color(212, 0, 0)
    lightred = pygame.Color(229, 102, 102)
    darkred = pygame.Color(170, 0, 0)
    green = pygame.Color(78, 185, 71)
    lightgreen = pygame.Color(106, 224, 97)
    darkgreen = pygame.Color(41, 126, 63)


class Game:
    def __init__(self, caption="Base game", width=800, height=600, framerate=60, strategy=None, code_hash=''):
        self.code_hash = code_hash
        self.interactive = strategy is None
        self.strategy = strategy or self.interactive_strategy()
        self.game_name = caption.lower().replace(' ', '_')
        with open('team_uuid.txt', 'r') as f:
            self.team_id = f.read().split('\n')[0].strip()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        pygame.display.set_caption(caption)
        self.window_surface = pygame.display.set_mode((width, height))
        self.width, self.height = width, height
        self.pressed_keys = set()
        self.now_pressed_keys = None
        self.is_running = True
        self.lose_background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.lose_background.fill(pygame.Color('#000000'))
        self.lose_background.set_alpha(80)
        self.win_background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.win_background.fill(pygame.Color('#ffffff'))
        self.win_background.set_alpha(80)
        self.empty_bar = pygame.image.load('assets/empty_bar.png')
        self.empty_bar = pygame.transform.scale(self.empty_bar, (180, 20))
        self.running_time = 0
        self.waiting_background = pygame.image.load('assets/waiting_background.png')
        self.waiting_background = pygame.transform.scale(self.waiting_background, (self.width, self.height))

    def focus(self):
        try:
            pass
        except:
            pass

        return self

    def run(self):
        started = False
        while not started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == 32:
                    started = True

            self.window_surface.blit(self.waiting_background, (0, 0))
            pygame.display.update()
            self.clock.tick(self.framerate)

        while self.is_running:
            self.now_pressed_keys = set()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    self.pressed_keys.add(event.key)
                    self.now_pressed_keys.add(event.key)
                elif event.type == pygame.KEYUP:
                    if event.key in self.pressed_keys:
                        self.pressed_keys.remove(event.key)

            self.render()
            dt = self.clock.tick(self.framerate)
            if dt < 200:
                dt_ms = dt / 1000
                self.running_time += dt_ms
                self.update_state(dt_ms)

            self.ingest_strategy(self.strategy(*self.get_strategy_parameters()))

            pygame.display.update()

    def handle_event(self, event):
        pass

    def render(self):
        pass

    def update_state(self, dt):
        pass

    def interactive_strategy(self):
        pass

    def ingest_strategy(self, *args):
        pass

    def get_strategy_parameters(self):
        return []

    def win(self):
        self.game_over(self.win_background)
        if not self.interactive:
            output = base64.b64encode((self.code_hash + json.dumps({
                'game': sha256_encode(f'{self.game_name}_{self.team_id}'.encode()),
                'datetime': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            })).encode()).decode()
            print(output)

    def lose(self):
        self.game_over(self.lose_background)

    def game_over(self, fade_out_surface):
        pygame.display.update()
        sleep(.4)
        for i in range(10):
            self.window_surface.blit(fade_out_surface, (0, 0))
            pygame.display.update()
            sleep(.05)
        self.is_running = False

    def show_win_percentage(self, percentage):
        self.window_surface.blit(self.empty_bar, (600, 30))
        pygame.draw.rect(self.window_surface, Colors.green,
                         (604, 36, int(173 * percentage), 9))
        pygame.draw.rect(self.window_surface, Colors.lightgreen,
                         (607, 34, int(173 * percentage) - 3, 2))
        pygame.draw.rect(self.window_surface, Colors.darkgreen,
                         (607, 45, int(173 * percentage) - 3, 3))

    def show_lose_percentage(self, percentage):
        self.window_surface.blit(self.empty_bar, (600, 50))
        pygame.draw.rect(self.window_surface, Colors.red,
                         (604, 56, int(173 * percentage), 9))
        pygame.draw.rect(self.window_surface, Colors.lightred,
                         (607, 54, int(173 * percentage) - 3, 2))
        pygame.draw.rect(self.window_surface, Colors.darkred,
                         (607, 65, int(173 * percentage) - 3, 3))
