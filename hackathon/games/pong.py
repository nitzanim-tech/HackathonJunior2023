import pygame,random,math
from .base_game import Game,Key,Point2D
PONG_SPEED=800
BALL_SPEED=1500
MARGIN=25
ANGLE_MARGIN=math.pi/6
PINGS_TO_FINISH=30
def sign(x):return 2*int(x>0)-1
class Pong(Game):
	def __init__(A,*C,**D):B='#e0b867';super().__init__(*(C),caption='PONG',**D);A.background=pygame.image.load('assets/pong/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.pong=pygame.image.load('assets/pong/pong.png');A.pong=pygame.transform.scale(A.pong,(150/A.pong.get_height()*A.pong.get_width(),150));A.pong_loc=Point2D(20,A.height//2);A.mirror=pygame.Surface((25,A.height));A.mirror.fill(pygame.Color(B));A.mirror_loc=Point2D(A.width-A.mirror.get_width(),0);A.wall=pygame.Surface((A.width,MARGIN));A.wall.fill(pygame.Color(B));A.ball=pygame.image.load('assets/pong/pool_ball.png');A.ball=pygame.transform.scale(A.ball,(60,60));A.ball_loc=Point2D(A.width//4,A.height//2);A.ball_angle=A.randomize_angle();A.direction=None;A.pings=0
	def randomize_angle(A):B=math.atan2(A.height//2,A.width//2);C=-B;return random.random()*(B-C)+C
	def render(A):A.window_surface.blit(A.background,(0,0));A.window_surface.blit(A.pong,A.pong_loc);A.window_surface.blit(A.ball,A.ball_loc);A.show_win_percentage(A.pings/PINGS_TO_FINISH)
	def interactive_strategy(A):
		def B(*B):
			if Key.ARROW_UP.value in A.pressed_keys:return 1
			elif Key.ARROW_DOWN.value in A.pressed_keys:return 2
			return None
		return B
	def ingest_strategy(A,direction):A.direction=direction
	def get_strategy_parameters(A):return[A.pong_loc.x+A.pong.get_width(),A.pong_loc.y,A.pong_loc.y+A.pong.get_height(),A.width-MARGIN,MARGIN,A.height-MARGIN,A.ball_loc.x,A.ball_loc.y,math.cos(A.ball_angle),math.sin(A.ball_angle)]
	def update_state(A,dt):
		if A.direction==1:A.pong_loc.y=max(MARGIN,A.pong_loc.y-PONG_SPEED*dt)
		elif A.direction==2:A.pong_loc.y=min(A.height-A.pong.get_height()-MARGIN,A.pong_loc.y+PONG_SPEED*dt)
		if A.ball_loc.x+A.ball.get_width()>=A.width-MARGIN and math.cos(A.ball_angle)>0 or(A.ball_loc.x<=A.pong_loc.x+A.pong.get_width()or A.ball_loc.x+A.ball.get_width()<=A.pong_loc.x+A.pong.get_width())and A.ball_loc.y>=A.pong_loc.y and A.ball_loc.y+A.ball.get_height()//2<=A.pong_loc.y+A.pong.get_height()and math.cos(A.ball_angle)<0:
			if math.cos(A.ball_angle)<0:A.pings+=1
			A.ball_angle=sign(A.ball_angle)*(math.pi-abs(A.ball_angle))+(2*random.random()-1)*math.pi/10
		elif(A.ball_loc.y<=MARGIN or A.ball_loc.y+A.ball.get_height()>=A.height-MARGIN)and sign(math.sin(A.ball_angle))==sign(A.ball_loc.y-A.height//2):A.ball_angle*=-1
		B=sign(A.ball_angle);A.ball_angle=abs(A.ball_angle)
		if A.ball_angle>math.pi/2-ANGLE_MARGIN and A.ball_angle<=math.pi/2:A.ball_angle=math.pi/2-ANGLE_MARGIN
		elif A.ball_angle>=math.pi/2 and A.ball_angle<math.pi/2+ANGLE_MARGIN:A.ball_angle=math.pi/2+ANGLE_MARGIN
		A.ball_angle*=B;A.ball_loc.x+=math.cos(A.ball_angle)*BALL_SPEED*dt;A.ball_loc.y+=math.sin(A.ball_angle)*BALL_SPEED*dt;A.ball_loc.x=min(A.ball_loc.x,A.width-MARGIN);A.ball_loc.y=max(MARGIN,min(A.ball_loc.y,A.height-MARGIN))
		if A.ball_loc.x+A.ball.get_width()<0:A.lose()
		if A.pings>=PINGS_TO_FINISH:A.win()
if __name__=='__main__':Pong().run()