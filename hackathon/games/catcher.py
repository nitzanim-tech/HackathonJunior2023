_A=None
import pygame,random
from .base_game import Game,Key,Point2D
CATCHER_SPEED=1200
BALL_SPEED=800
BALLS_TO_CATCH=20
class Catcher(Game):
	def __init__(A,*B,**C):super().__init__(*(B),caption='CATCHER',**C);A.background=pygame.image.load('assets/catcher/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.catcher=pygame.image.load('assets/catcher/treasure_chest.png');A.catcher=pygame.transform.scale(A.catcher,(250,int(250/A.catcher.get_width()*A.catcher.get_height())));A.catcher_loc=Point2D(A.width//2-A.catcher.get_width()//2,A.height-A.catcher.get_height()-20);A.ball=pygame.image.load('assets/catcher/coin.png');A.ball=pygame.transform.scale(A.ball,(A.ball.get_width()//2,A.ball.get_height()//2));A.ball_loc=_A;A.direction=_A;A.balls_caught=0
	def render(A):
		A.window_surface.blit(A.background,(0,0));A.window_surface.blit(A.catcher,A.catcher_loc)
		if A.ball_loc is not _A:A.window_surface.blit(A.ball,A.ball_loc)
		A.show_win_percentage(A.balls_caught/BALLS_TO_CATCH)
	def interactive_strategy(A):
		def B(catcher_left,catcher_right,ball_left,ball_right):
			if Key.ARROW_LEFT.value in A.pressed_keys:return 1
			if Key.ARROW_RIGHT.value in A.pressed_keys:return 2
		return B
	def ingest_strategy(A,direction):A.direction=direction
	def get_strategy_parameters(A):return[A.catcher_loc.x,A.catcher_loc.x+A.catcher.get_width(),A.ball_loc.x if A.ball_loc is not _A else _A,A.ball_loc.x+A.ball.get_width()if A.ball_loc is not _A else _A]
	def update_state(A,dt):
		if A.direction==1:A.catcher_loc.x=max(0,A.catcher_loc.x-CATCHER_SPEED*dt)
		if A.direction==2:A.catcher_loc.x=min(A.width-A.catcher.get_width(),A.catcher_loc.x+CATCHER_SPEED*dt)
		if A.ball_loc is _A and random.random()<=0.05:A.ball_loc=Point2D(random.randint(0,A.width-A.ball.get_width()),0)
		if A.ball_loc is not _A:A.ball_loc.y+=BALL_SPEED*dt
		if A.ball_loc is not _A:
			if A.ball_loc.y>A.catcher_loc.y+A.catcher.get_height()//3 and A.ball_loc.y<A.catcher_loc.y+A.catcher.get_height()and A.ball_loc.x+A.ball.get_width()>=A.catcher_loc.x and A.ball_loc.x<=A.catcher_loc.x+A.catcher.get_width():A.ball_loc=_A;A.balls_caught+=1
			elif A.ball_loc.y>A.height:A.lose()
		if A.balls_caught>=BALLS_TO_CATCH:A.win()
if __name__=='__main__':Catcher().run()