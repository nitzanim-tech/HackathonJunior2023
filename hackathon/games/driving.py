_A=None
import pygame
from .base_game import Game,Key,Point2D
import math,random
from pygame import gfxdraw
GAS_FORCE=20
FRICTION_MU=10
H=16
N=2000
SIZE=5000
SENSOR_THETAS=[-math.pi/4,-math.pi/8,0,math.pi/8,math.pi/4]
SENSOR_OFFSET=40
MAX_SENSOR_DISTNACE=1000
MIN_SENSOR_DISTANCE_FOR_STOPPING=15
EPSILON=1e-05
STEER_MAGNITUDE=math.pi/50
CHECKPOINT_COLLECTION_RADIUS=200
TIME_TO_FINISH=30
MAX_SPEED=2700
def sign(x):
	if x==0:return 0
	return 2*(int(x>0)-0.5)
def line_intersection(l1_p1,l1_p2,l2_p1,l2_p2):
	A,B=l1_p1;C,D=l1_p2;E,F=l2_p1;G,H=l2_p2;K=(A-C)*(F-H)-(B-D)*(E-G)
	if K==0:return _A
	I=((A*D-B*C)*(E-G)-(A-C)*(E*H-F*G))/K;J=((A*D-B*C)*(F-H)-(B-D)*(E*H-F*G))/K
	if I<min(A,C)-EPSILON or I>max(A,C)+EPSILON or I<min(E,G)-EPSILON or I>max(E,G)+EPSILON or J<min(B,D)-EPSILON or J>max(B,D)+EPSILON or J<min(F,H)-EPSILON or J>max(F,H)+EPSILON:return _A
	return I,J
def normsq(x,y):return x**2+y**2
def randomize_track_curves(center_x,center_y,scale,gap):
	F=center_y;E=center_x;D=gap;Q=[10**(-0.5-2*A/(H-1))*random.random()for A in range(H)];R=[random.random()*2*math.pi for A in range(H)];C=[A/(N-1)*2*math.pi for A in range(N)];B=[1.2 for A in range(N)]
	for G in range(H):
		for A in range(N):B[A]=B[A]+Q[G]*math.sin(G*C[A]+R[G])
	for A in range(N):B[A]*=scale
	I,J=[],[];K,L=[],[];M,O=[],[]
	for A in range(N):I.append(B[A]*math.cos(C[A])+E);J.append(B[A]*math.sin(C[A])+F);K.append((B[A]-D)*math.cos(C[A])+E);L.append((B[A]-D)*math.sin(C[A])+F);M.append((B[A]+D)*math.cos(C[A])+E);O.append((B[A]+D)*math.sin(C[A])+F)
	for P in [I,J,K,L,M,O]:P.append(P[0])
	return I,J,K,L,M,O
def create_background():
	A=pygame.image.load('assets/driving/background.png');A=pygame.transform.scale(A,(A.get_width()//2,A.get_height()//2));B=pygame.Surface((SIZE*2.5,SIZE*2.5))
	for C in range(math.ceil(B.get_height()/A.get_height())):
		for D in range(math.ceil(B.get_width()/A.get_width())):B.blit(A,(D*A.get_width(),C*A.get_height()))
	return B
class Driving(Game):
	def __init__(A,*B,**C):super().__init__(*(B),caption='Driving',**C);A.x,A.y,A.xin,A.yin,A.xout,A.yout=randomize_track_curves(SIZE,SIZE,SIZE/2,120);A.background=create_background();A.car_loc=Point2D(A.x[0],A.y[0]);A.car=pygame.image.load('assets/driving/car.png');A.car=pygame.transform.scale(A.car,(A.car.get_width()//1.5,A.car.get_height()//1.5));gfxdraw.filled_polygon(A.background,list(zip(A.xin,A.yin))+list(zip(A.xout,A.yout))[::-1],pygame.Color('#333344'));A.speed=0;A.direction=3*math.pi/2;A.gas=0;A.steer=0;A.sensor_distances=[MAX_SENSOR_DISTNACE for A in SENSOR_THETAS];A.uncollected_checkpoints=set(zip(A.x,A.y))
	def render(A):
		B=pygame.transform.rotate(A.car.copy(),180-A.direction*180/math.pi);A.window_surface.blit(A.background,(A.width//2-A.car_loc.x,A.height//2-A.car_loc.y));A.window_surface.blit(B,(A.width//2-B.get_width()//2,A.height//2-B.get_height()//2))
		for (C,D) in zip(SENSOR_THETAS,A.sensor_distances):pygame.draw.line(A.window_surface,pygame.Color('#ffffff'),(A.width//2+SENSOR_OFFSET*math.cos(A.direction),A.height//2+SENSOR_OFFSET*math.sin(A.direction)),(A.width//2+SENSOR_OFFSET*math.cos(A.direction)+D*math.cos(A.direction+C),A.height//2+SENSOR_OFFSET*math.sin(A.direction)+D*math.sin(A.direction+C)))
		A.show_win_percentage(1-len(A.uncollected_checkpoints)/len(A.x));A.show_lose_percentage(1-A.running_time/TIME_TO_FINISH)
	def interactive_strategy(A):
		def B(*D):
			C=0;B=0
			if Key.ARROW_UP.value in A.pressed_keys:C=1
			if Key.ARROW_LEFT.value in A.pressed_keys:B-=1
			if Key.ARROW_RIGHT.value in A.pressed_keys:B+=1
			return C,B
		return B
	def ingest_strategy(A,actions):A.gas,A.steer=actions
	def get_strategy_parameters(A):return[A.speed,*A.sensor_distances]
	def update_state(A,dt):
		A.direction+=A.steer*STEER_MAGNITUDE;A.speed=min(MAX_SPEED,max(A.speed+A.gas*GAS_FORCE-FRICTION_MU,0))
		if min(A.sensor_distances)<MIN_SENSOR_DISTANCE_FOR_STOPPING:A.speed=0
		A.car_loc.x+=A.speed*math.cos(A.direction)*dt;A.car_loc.y+=A.speed*math.sin(A.direction)*dt;A.sensor_distances=[A.calculate_sensor_distance((A.car_loc.x+SENSOR_OFFSET*math.cos(A.direction),A.car_loc.y+SENSOR_OFFSET*math.sin(A.direction)),B)for B in SENSOR_THETAS];A.uncollected_checkpoints-={B for B in A.uncollected_checkpoints if normsq(B[0]-A.car_loc.x,B[1]-A.car_loc.y)<=CHECKPOINT_COLLECTION_RADIUS**2}
		if len(A.uncollected_checkpoints)==0:A.win()
		elif A.running_time>=TIME_TO_FINISH:A.lose()
	def calculate_sensor_distance(A,sensor_origin,theta):
		H=theta;C=sensor_origin;D=C[0]+MAX_SENSOR_DISTNACE*math.cos(A.direction+H),C[1]+MAX_SENSOR_DISTNACE*math.sin(A.direction+H)
		for B in range(len(A.xin)-1):
			F=A.xin[B],A.yin[B];G=A.xin[B+1],A.yin[B+1];E=line_intersection(C,D,F,G)
			if E is not _A:D=E
		for B in range(len(A.xout)-1):
			F=A.xout[B],A.yout[B];G=A.xout[B+1],A.yout[B+1];E=line_intersection(C,D,F,G)
			if E is not _A:D=E
		return math.sqrt(math.pow(D[0]-C[0],2)+math.pow(D[1]-C[1],2))
if __name__=='__main__':Driving().run()