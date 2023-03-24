_A=None
import pygame
from .base_game import Game,Key
import random
GRID_LEFT=150
GRID_TOP=50
GRID_SIDE=500
GRID_CELLS=25
GRID_CELL_SIDE=GRID_SIDE/GRID_CELLS
DIRECTIONS=[(1,0),(-1,0),(0,1),(0,-1)]
DIRECTION_ANGLES=[0,180,90,270]
ACTION_DIRECTIONS={Key.ARROW_LEFT.value:3,Key.ARROW_RIGHT.value:2,Key.ARROW_UP.value:1,Key.ARROW_DOWN.value:0}
LENGTH_TO_FINISH=32
class Snake(Game):
	def __init__(A,*D,**E):
		C='#6a839b';super().__init__(*(D),caption='Snake',framerate=10,**E);A.background=pygame.image.load('assets/snake/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));pygame.draw.rect(A.background,pygame.Color('#ceddee'),(GRID_LEFT,GRID_TOP,GRID_SIDE,GRID_SIDE))
		for F in range(GRID_CELLS+1):B=F*GRID_CELL_SIDE;pygame.draw.line(A.background,pygame.Color(C),(GRID_LEFT,GRID_TOP+B),(GRID_LEFT+GRID_SIDE,GRID_TOP+B),width=1);pygame.draw.line(A.background,pygame.Color(C),(GRID_LEFT+B,GRID_TOP),(GRID_LEFT+B,GRID_TOP+GRID_SIDE),width=1)
		A.snake=[(0,0),(0,1),(0,2)];A.direction_index=2;A.snake_rect=pygame.image.load('assets/snake/snake_body.png');A.snake_rect=pygame.transform.scale(A.snake_rect,(GRID_CELL_SIDE-2,GRID_CELL_SIDE-2));A.snake_head=pygame.image.load('assets/snake/snake_head.png');A.snake_head=pygame.transform.scale(A.snake_head,(GRID_CELL_SIDE-2,GRID_CELL_SIDE-2));A.food_pos=_A;A.randomize_food();A.food_rect=pygame.image.load('assets/snake/apple.png');A.food_rect=pygame.transform.scale(A.food_rect,(GRID_CELL_SIDE-2,GRID_CELL_SIDE-2))
	def randomize_food(A):
		A.food_pos=_A
		while A.food_pos is _A or A.food_pos in A.snake:A.food_pos=random.randint(0,GRID_CELLS-1),random.randint(0,GRID_CELLS-1)
	def render(A):
		A.window_surface.blit(A.background,(0,0))
		for (C,(D,E)) in enumerate(A.snake):
			B=A.snake_rect
			if C+1==len(A.snake):B=A.snake_head.copy();B=pygame.transform.rotate(B,DIRECTION_ANGLES[A.direction_index])
			A.window_surface.blit(B,(GRID_LEFT+GRID_CELL_SIDE*E+1,GRID_TOP+GRID_CELL_SIDE*D+1))
		A.window_surface.blit(A.food_rect,(GRID_LEFT+GRID_CELL_SIDE*A.food_pos[1]+1,GRID_TOP+GRID_CELL_SIDE*A.food_pos[0]+1));A.show_win_percentage(len(A.snake)/LENGTH_TO_FINISH)
	def interactive_strategy(A):
		def B(*B):return[ACTION_DIRECTIONS[A]for A in A.now_pressed_keys if A in ACTION_DIRECTIONS]
		return B
	def ingest_strategy(B,new_direction):
		A=new_direction
		if A is _A:return
		if not isinstance(A,list):A=[A]
		A=list(filter(lambda direction:sum([DIRECTIONS[B.direction_index][A]+DIRECTIONS[direction][A]==0 for A in range(2)])!=2,A))
		if len(A)==0:return
		B.direction_index=A[0]
	def get_strategy_parameters(A):return[A.snake,A.food_pos,A.direction_index,GRID_CELLS]
	def update_state(A,dt):
		for C in range(len(A.snake)-1):A.snake[C]=A.snake[C+1]
		D=A.snake[0];B=list(A.snake[-1]);B[0]+=DIRECTIONS[A.direction_index][0];B[1]+=DIRECTIONS[A.direction_index][1];B=tuple(B)
		if B[0]<0 or B[0]>=GRID_CELLS or B[1]<0 or B[1]>=GRID_CELLS or B in A.snake[:-1]:A.lose();return
		A.snake[-1]=B
		if A.snake[-1]==A.food_pos:A.randomize_food();A.snake.insert(0,D)
		if len(A.snake)>=LENGTH_TO_FINISH:A.win()
if __name__=='__main__':Snake().run()