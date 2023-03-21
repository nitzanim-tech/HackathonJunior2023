import pygame
from .base_game import Game, Key, Point2D


class TemplateGame(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, caption="???", **kwargs)
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color("#5f306b"))

    def render(self):
        self.window_surface.blit(self.background, (0, 0))

    def interactive_strategy(self):
        def action(*args):
            pass

        return action

    def ingest_strategy(self, *args):
        pass

    def get_strategy_parameters(self):
        return [

        ]

    def update_state(self, dt):
        pass


if __name__ == '__main__':
    TemplateGame().run()
