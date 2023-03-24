_A=None
import pygame,random
from .base_game import Game,Key,Point2D
CATCHER_SPEED=1200
BALL_SPEED=800
BALLS_TO_CATCH=30
class DoubleCatcher(Game):
	def __init__(A,*C,**D):
		super().__init__(*(C),caption='DOUBLE CATCHER',**D);A.background=pygame.image.load('assets/catcher/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.catchers=[pygame.image.load('assets/catcher/treasure_chest.png')for A in range(2)]
		for B in range(len(A.catchers)):A.catchers[B]=pygame.transform.scale(A.catchers[B],(125,int(125/A.catchers[B].get_width()*A.catchers[B].get_height())))
		A.catcher_locs=[Point2D(A.width//3-A.catchers[0].get_width()//2,A.height-A.catchers[0].get_height()-20),Point2D(2*A.width//3-A.catchers[0].get_width()//2,A.height-A.catchers[0].get_height()-20)][::-1];A.balls=[pygame.image.load('assets/catcher/coin.png')for A in range(2)]
		for B in range(len(A.balls)):A.balls[B]=pygame.transform.scale(A.balls[B],(A.balls[B].get_width()//2,A.balls[B].get_height()//2))
		A.ball_locs=[_A,_A];A.direction1=_A;A.direction2=_A;A.balls_caught=0
	def render(A):
		A.window_surface.blit(A.background,(0,0))
		for (C,D) in zip(A.catchers,A.catcher_locs):A.window_surface.blit(C,D)
		for (B,E) in zip(A.ball_locs,A.balls):
			if B is not _A:A.window_surface.blit(E,B)
		A.show_win_percentage(A.balls_caught/BALLS_TO_CATCH)
	def interactive_strategy(A):
		def B(catcher1_left,catcher1_right,catcher2_left,catcher2_right,ball1_left,ball1_right,ball2_left,ball2_right):
			B=_A;C=_A
			if Key.ARROW_LEFT.value in A.pressed_keys:B=1
			elif Key.ARROW_RIGHT.value in A.pressed_keys:B=2
			if ord('a')in A.pressed_keys:C=1
			elif ord('d')in A.pressed_keys:C=2
			return B,C
		return B
	def ingest_strategy(A,directions):
		B=directions
		if B is not _A:A.direction1,A.direction2=B
	def get_strategy_parameters(A):return sum([[A.x,A.x+B.get_width()]for(B,A)in zip(A.catchers,A.catcher_locs)],[])+sum([[A.x if A is not _A else _A,A.x+B.get_width()if A is not _A else _A]for(B,A)in zip(A.balls,A.ball_locs)],[])
	def update_state(A,dt):
		C=dt
		if A.direction1==1:A.catcher_locs[0].x=max(0,A.catcher_locs[0].x-CATCHER_SPEED*C)
		if A.direction1==2:A.catcher_locs[0].x=min(A.width-A.catchers[0].get_width(),A.catcher_locs[0].x+CATCHER_SPEED*C)
		if A.direction2==1:A.catcher_locs[1].x=max(0,A.catcher_locs[1].x-CATCHER_SPEED*C)
		if A.direction2==2:A.catcher_locs[1].x=min(A.width-A.catchers[1].get_width(),A.catcher_locs[1].x+CATCHER_SPEED*C)
		for B in range(len(A.ball_locs)):
			if A.ball_locs[B]is _A and random.random()<=0.05:A.ball_locs[B]=Point2D(random.randint(0,A.width-A.balls[B].get_width()),0)
			if A.ball_locs[B]is not _A:A.ball_locs[B].y+=BALL_SPEED*C
			if A.ball_locs[B]is not _A:
				E=False
				for D in A.catcher_locs:
					if A.ball_locs[B].y>D.y and A.ball_locs[B].y<D.y+A.catchers[0].get_height()and A.ball_locs[B].x>=D.x and A.ball_locs[B].x<=D.x+A.catchers[0].get_width():E=True;break
				if E:A.ball_locs[B]=_A;A.balls_caught+=1
				elif A.ball_locs[B].y>A.height:A.lose()
			if A.balls_caught>=BALLS_TO_CATCH:A.win()
if __name__=='__main__':DoubleCatcher().run()