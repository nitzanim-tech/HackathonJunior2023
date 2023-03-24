import os
from glob import glob
import hashlib
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
def get_files_hash(paths):
	A=hashlib.sha256()
	for B in paths:
		with open(B,'r')as C:A.update(C.read().encode())
	return A.hexdigest()
def main():
	B=[Catcher,DoubleCatcher,Pong,CartPole,MountainCar,Snake,FlappyBird,Driving];D=[catcher_strategy,double_catcher_strategy,pong_strategy,cartpole_strategy,mountaincar_strategy,snake_strategy,flappy_bird_strategy,driving_strategy];E=get_files_hash([__file__]+glob(os.path.join(os.path.split(__file__)[0],'games','*.py'),recursive=True));A=-1
	while A<0 or A>=len(B):
		print('Choose your game:');print('\n'.join([f"{A+1}) {B.__name__}"for(A,B)in enumerate(B)]))
		try:A=int(input('Game #: '))-1
		except ValueError:pass
	C=None
	while C not in{'S','P'}:C=input('[P]layer or [S]trategic mode? ').upper()
	F=None if C=='P'else D[A];B[A](strategy=F,code_hash=E).focus().run()
if __name__=='__main__':main()