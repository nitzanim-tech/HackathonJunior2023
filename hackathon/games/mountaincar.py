import pygame
from .base_game import Game,Key,Point2D
import math
START_X=330
RADIUS=20
FORCE=70
FRICTION_MU=60
G=200
FLAG_X=740
TIME_TO_FINISH=32
def sign(x):
	if x==0:return 0
	return 2*(int(x>0)-0.5)
def ground(x):x=(x-340)/300;return 500+200*(x**3-2*x**2)
def ground_dot(x):x=(x-340)/300;return 200*(3*x**2-4*x)/300
def draw_ground(surface):
	B=surface;C=int(ground(0))
	for A in range(1,B.get_width()+1):D=int(ground(A));pygame.draw.line(B,pygame.Color('#ffffff'),(A-1,C),(A,D));C=D
class MountainCar(Game):
	def __init__(A,*B,**C):super().__init__(*(B),caption='MountainCar',**C);A.background=pygame.image.load('assets/mountaincar/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.car_loc=Point2D(START_X,ground(START_X));A.x_dot=0;A.direction=None;A.flag=pygame.image.load('assets/mountaincar/flag.png');A.flag=pygame.transform.scale(A.flag,(A.flag.get_width()//1.5,A.flag.get_height()//1.5));A.car=pygame.image.load('assets/mountaincar/car.png');A.car=pygame.transform.scale(A.car,(A.car.get_width()//1.5,A.car.get_height()//1.5));A.x_dotdot=0
	def render(A):
		C=ground_dot(A.car_loc.x);B=-0.5*math.pi
		if C!=0:B=math.atan(-1/C)
		if B>0:B+=math.pi
		E=math.cos(B)*A.car.get_height()/2;F=math.sin(B)*A.car.get_height()/2;A.window_surface.blit(A.background,(0,0));D=pygame.transform.rotate(A.car,-math.atan(C)*180/math.pi);A.window_surface.blit(D,(A.car_loc.x-D.get_width()//2+E,A.car_loc.y-D.get_height()//2+F));A.window_surface.blit(A.flag,(FLAG_X,ground(FLAG_X)-A.flag.get_height()));A.show_lose_percentage(1-A.running_time/TIME_TO_FINISH)
	def interactive_strategy(A):
		def B(*B):
			if Key.ARROW_LEFT.value in A.pressed_keys:return 1
			elif Key.ARROW_RIGHT.value in A.pressed_keys:return 2
			return None
		return B
	def ingest_strategy(A,direction):A.direction=direction
	def get_strategy_parameters(A):return[A.x_dot,A.x_dotdot]
	def update_state(A,dt):
		dt*=2;B=-1 if A.direction==1 else 1 if A.direction==2 else 0;A.x_dotdot=G*ground_dot(A.car_loc.x)-sign(A.x_dot)*FRICTION_MU+B*FORCE;A.x_dot+=A.x_dotdot*dt;A.car_loc.x+=A.x_dot*dt;A.car_loc.y=ground(A.car_loc.x)
		if A.car_loc.x>=FLAG_X:A.win()
		if A.running_time>=TIME_TO_FINISH:A.lose()
if __name__=='__main__':MountainCar().run()