from games.catcher import Catcher
from games.double_catcher import DoubleCatcher
from games.pong import Pong
from games.cartpole import CartPole
from games.mountaincar import MountainCar
from games.snake import Snake
from games.flappy_bird import FlappyBird
from games.driving import Driving
from strategies.catcher import action as catcher_strategy
from strategies.double_catcher import action as double_catcher_strategy
from strategies.pong import action as pong_strategy
from strategies.cartpole import action as cartpole_strategy
from strategies.mountaincar import action as mountaincar_strategy
from strategies.snake import action as snake_strategy
from strategies.flappy_bird import action as flappy_bird_strategy
from strategies.driving import action as driving_strategy


def main():
    games = [Catcher, DoubleCatcher, Pong, CartPole, MountainCar, Snake, FlappyBird, Driving]
    strategies = [catcher_strategy, double_catcher_strategy, pong_strategy, cartpole_strategy, mountaincar_strategy,
                  snake_strategy, flappy_bird_strategy, driving_strategy]

    game_idx = -1
    while game_idx < 0 or game_idx >= len(games):
        print("Choose your game:")
        print("\n".join([f"{i + 1}) {game.__name__}" for i, game in enumerate(games)]))
        try:
            game_idx = int(input("Game #: ")) - 1
        except ValueError:
            pass

    mode = None
    while mode not in {'S', 'P'}:
        mode = input("[P]layer or [S]trategic mode? ").upper()

    strategy = None if mode == 'P' else strategies[game_idx]
    games[game_idx](strategy=strategy).focus().run()


if __name__ == "__main__":
    main()
