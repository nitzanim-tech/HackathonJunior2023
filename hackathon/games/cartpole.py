import pygame
from .base_game import Game,Key,Point2D
import math,random
L=250
M_C=20
M_P=5
G=10
MU_C=0.05
MU_P=0.0
F=100000
MAX_THETA=math.pi/2*0.8
TIME_TO_SURVIVE=20
HAND_OFFSET=65
def sign(x):
	if x==0:return 0
	return 2*int(x>0)-1
class CartPole(Game):
	def __init__(A,*B,**C):super().__init__(*(B),caption='CARTPOLE',**C);A.background=pygame.image.load('assets/cartpole/background.png');A.background=pygame.transform.scale(A.background,(A.width,A.height));A.cart=pygame.image.load('assets/cartpole/boy.png');A.cart_loc=Point2D(A.width//2-A.cart.get_width()//2,A.height-A.cart.get_height()-70);A.move=None;A.force=0;A.pole_head=pygame.image.load('assets/cartpole/plate.png');A.pole_head=pygame.transform.scale(A.pole_head,(70,70/A.pole_head.get_width()*A.pole_head.get_height()));A.pole_head_loc=Point2D(A.cart_loc.x+A.cart.get_width()//2-A.pole_head.get_width()//2+HAND_OFFSET,A.cart_loc.y-L-A.pole_head.get_height());A.theta=(random.random()-0.5)/5;A.theta_dot=0;A.theta_dotdot=0;A.x_dot=0;A.x_dotdot=0;A.n_c=1
	def render(A):B=Point2D(A.cart_loc.x+A.cart.get_width()//2+HAND_OFFSET,A.cart_loc.y+10);A.window_surface.blit(A.background,(0,0));pygame.draw.line(A.window_surface,pygame.Color('#111111'),B,(A.pole_head_loc.x+A.pole_head.get_width()//2,A.pole_head_loc.y+A.pole_head.get_height()//2));A.window_surface.blit(A.cart,A.cart_loc);A.window_surface.blit(A.pole_head,A.pole_head_loc);A.show_win_percentage(A.running_time/TIME_TO_SURVIVE)
	def interactive_strategy(A):
		def B(*B):
			if Key.ARROW_LEFT.value in A.now_pressed_keys:return 1
			elif Key.ARROW_RIGHT.value in A.now_pressed_keys:return 2
			return None
		return B
	def ingest_strategy(A,move):A.move=move
	def get_strategy_parameters(A):return[A.cart_loc.x,A.cart_loc.x+A.cart.get_width(),A.x_dot,*A.pole_head_loc,L*math.sin(A.theta),L*math.cos(A.theta)]
	def update_state(A,dt):
		B=dt;B*=2
		if A.move==1:A.force=-F
		elif A.move==2:A.force=F
		else:A.force=0
		C=(M_C+M_P)*G-M_P*L*(A.theta_dotdot*math.sin(A.theta)+A.theta_dot**2*math.cos(A.theta));A.theta_dotdot=(G*math.sin(A.theta)+math.cos(A.theta)*((-A.force-M_P*L*A.theta_dot**2*(math.sin(A.theta)+MU_C*sign(C*A.x_dot)*math.cos(A.theta)))/(M_P+M_C)+MU_C*G*sign(C*A.x_dot))-MU_P*A.theta_dot/(M_P*L))/(L*(4/3-M_P*math.cos(A.theta)/(M_C+M_P)*(math.cos(A.theta)-MU_C*sign(C*A.x_dot))));A.x_dotdot=(A.force+M_P*L*(A.theta_dot**2*math.sin(A.theta)-A.theta_dotdot*math.cos(A.theta))-MU_C*C*sign(C*A.x_dot))/(M_C+M_P);A.theta_dot+=A.theta_dotdot*B;A.x_dot+=A.x_dotdot*B;A.theta+=A.theta_dot*B;A.cart_loc.x+=A.x_dot*B;A.pole_head_loc.x=A.cart_loc.x+A.cart.get_width()//2-A.pole_head.get_width()//2+math.sin(A.theta)*L+HAND_OFFSET;A.pole_head_loc.y=A.cart_loc.y-math.cos(A.theta)*L
		if abs(A.theta)>MAX_THETA or A.cart_loc.x<0 or A.cart_loc.x+A.cart.get_width()>A.width:A.lose()
		if A.running_time>=TIME_TO_SURVIVE:A.win()
if __name__=='__main__':CartPole().run()