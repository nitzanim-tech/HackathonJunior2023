_B=False
_A=None
import pygame
from .base_game import Game,Key,Point2D
import random
G=1000
FORCE=-45000
PIPE_SPEED=150
PIPE_GAP_HEIGHT_RATIO=0.4
TIME_TO_SURVIVE=25
class FlappyBird(Game):
	def __init__(A,*B,**C):super().__init__(*(B),caption='Flappy Bird',**C);A.background=pygame.image.load('assets/flappy_bird/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.bird_loc=Point2D(200,200);A.y_dot=-500;A.bird=pygame.image.load('assets/flappy_bird/bat.png');A.bird=pygame.transform.scale(A.bird,(70/A.bird.get_height()*A.bird.get_width(),70));A.bird_flap=pygame.image.load('assets/flappy_bird/bat_flap.png');A.bird_flap=pygame.transform.scale(A.bird_flap,(70/A.bird_flap.get_height()*A.bird_flap.get_width(),70));A.flap=_B;A.pipes=[];A.pipe=pygame.image.load('assets/flappy_bird/pipe.png');A.background_offset_x=0;A.time_since_last_flap=0
	def render(A):
		A.window_surface.blit(A.background,(A.background_offset_x,0));A.window_surface.blit(A.background,(A.background_offset_x+A.background.get_width(),0));B=A.bird
		if A.time_since_last_flap<0.3:B=A.bird_flap
		A.window_surface.blit(B,(A.bird_loc[0]-A.bird.get_width()//2,A.bird_loc[1]-A.bird.get_height()//2))
		for (C,D) in A.pipes:A.window_surface.blit(pygame.transform.flip(A.pipe,_B,True),(C-A.pipe.get_width()//2,D-A.pipe.get_height()));A.window_surface.blit(A.pipe,(C-A.pipe.get_width()//2,D+PIPE_GAP_HEIGHT_RATIO*A.height))
		A.show_win_percentage(A.running_time/TIME_TO_SURVIVE)
	def interactive_strategy(A):
		def B(*B):
			if ord(' ')in A.now_pressed_keys:return 1
			return _A
		return B
	def ingest_strategy(A,flap):A.flap=flap==1
	def get_strategy_parameters(A):
		B=[(B-A.bird_loc.x-A.bird.get_width()//2-A.pipe.get_width()//2,C+A.bird.get_height()//2,C+PIPE_GAP_HEIGHT_RATIO*A.height-A.bird.get_height()//2)for(B,C)in A.pipes if B+A.pipe.get_width()//2>A.bird_loc.x-A.bird.get_width()//2];C=_A,_A,_A
		if len(B)>0:C=B[0]
		return[A.bird_loc.y,A.y_dot,*(C)]
	def update_state(A,dt):
		B=dt;A.time_since_last_flap+=B
		if A.flap:A.time_since_last_flap=0
		A.y_dot+=B*G+B*A.flap*FORCE;A.bird_loc.y+=B*A.y_dot;A.flap=_B
		if A.bird_loc.y-A.bird.get_height()//2<0 or A.bird_loc.y+A.bird.get_height()//2>A.height:A.lose()
		C=0
		while C<len(A.pipes):
			A.pipes[C][0]-=PIPE_SPEED*B
			if A.pipes[C][0]<0:del A.pipes[C]
			else:C+=1
		A.background_offset_x-=PIPE_SPEED*B
		if A.background_offset_x<=-A.background.get_width():A.background_offset_x=0
		if(len(A.pipes)==0 or A.pipes[-1][0]<0.6*A.width)and random.random()<=0.03:A.pipes.append([A.width,random.random()*0.3*A.height])
		for (E,D) in A.pipes:
			if abs(E-A.bird_loc.x)<=A.pipe.get_width()//2+A.bird.get_width()//2 and(A.bird_loc.y-A.bird.get_height()//2<D or A.bird_loc.y+A.bird.get_height()//2>D+PIPE_GAP_HEIGHT_RATIO*A.height):A.lose();break
		if A.running_time>=TIME_TO_SURVIVE:A.win()
if __name__=='__main__':FlappyBird().run()