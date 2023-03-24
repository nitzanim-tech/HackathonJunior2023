_A=False
import pygame
from enum import Enum
from time import sleep
import json,hashlib,base64
from datetime import datetime
def sha256_encode(text):A=hashlib.sha256();A.update(text);return A.hexdigest()
class Point2D:
	def __init__(A,x,y):A.x=x;A.y=y
	def __getitem__(A,idx):
		if idx==0:return A.x
		elif idx==1:return A.y
		raise ValueError('Point2D only has two coordinates')
	def __len__(A):return 2
	def __iter__(A):yield from[A[B]for B in range(len(A))]
class Key(Enum):ARROW_LEFT=1073741904;ARROW_RIGHT=1073741903;ARROW_UP=1073741906;ARROW_DOWN=1073741905;SPACE=32
class Colors:red=pygame.Color(212,0,0);lightred=pygame.Color(229,102,102);darkred=pygame.Color(170,0,0);green=pygame.Color(78,185,71);lightgreen=pygame.Color(106,224,97);darkgreen=pygame.Color(41,126,63)
class Game:
	def __init__(A,caption='Base game',width=800,height=600,framerate=60,strategy=None,code_hash=''):
		E=strategy;D=height;C=width;B=caption;A.code_hash=code_hash;A.interactive=E is None;A.strategy=E or A.interactive_strategy();A.game_name=B.lower().replace(' ','_')
		with open('team_uuid.txt','r')as F:A.team_id=F.read().split('\n')[0].strip()
		pygame.init();A.clock=pygame.time.Clock();A.framerate=framerate;pygame.display.set_caption(B);A.window_surface=pygame.display.set_mode((C,D));A.width,A.height=C,D;A.pressed_keys=set();A.now_pressed_keys=None;A.is_running=True;A.lose_background=pygame.Surface((A.width,A.height),pygame.SRCALPHA,32).convert_alpha();A.lose_background.fill(pygame.Color('#000000'));A.lose_background.set_alpha(80);A.win_background=pygame.Surface((A.width,A.height),pygame.SRCALPHA,32).convert_alpha();A.win_background.fill(pygame.Color('#ffffff'));A.win_background.set_alpha(80);A.empty_bar=pygame.image.load('assets/empty_bar.png');A.empty_bar=pygame.transform.scale(A.empty_bar,(180,20));A.running_time=0;A.waiting_background=pygame.image.load('assets/waiting_background.png');A.waiting_background=pygame.transform.scale(A.waiting_background,(A.width,A.height))
	def focus(A):
		try:0
		except:pass
		return A
	def run(A):
		C=_A
		while not C:
			for B in pygame.event.get():
				if B.type==pygame.QUIT:return
				elif B.type==pygame.KEYDOWN and B.key==32:C=True
			A.window_surface.blit(A.waiting_background,(0,0));pygame.display.update();A.clock.tick(A.framerate)
		while A.is_running:
			A.now_pressed_keys=set()
			for B in pygame.event.get():
				if B.type==pygame.QUIT:A.is_running=_A
				A.handle_event(B)
				if B.type==pygame.KEYDOWN:A.pressed_keys.add(B.key);A.now_pressed_keys.add(B.key)
				elif B.type==pygame.KEYUP:
					if B.key in A.pressed_keys:A.pressed_keys.remove(B.key)
			A.render();D=A.clock.tick(A.framerate)
			if D<200:E=D/1000;A.running_time+=E;A.update_state(E)
			A.ingest_strategy(A.strategy(*A.get_strategy_parameters()));pygame.display.update()
	def handle_event(A,event):0
	def render(A):0
	def update_state(A,dt):0
	def interactive_strategy(A):0
	def ingest_strategy(A,*B):0
	def get_strategy_parameters(A):return[]
	def win(A):
		A.game_over(A.win_background)
		if not A.interactive:B=base64.b64encode((A.code_hash+json.dumps({'game':sha256_encode(f"{A.game_name}_{A.team_id}".encode()),'datetime':datetime.now().strftime('%d-%m-%Y %H:%M:%S')})).encode()).decode();print(B)
	def lose(A):A.game_over(A.lose_background)
	def game_over(A,fade_out_surface):
		pygame.display.update();sleep(0.4)
		for B in range(10):A.window_surface.blit(fade_out_surface,(0,0));pygame.display.update();sleep(0.05)
		A.is_running=_A
	def show_win_percentage(A,percentage):B=percentage;A.window_surface.blit(A.empty_bar,(600,30));pygame.draw.rect(A.window_surface,Colors.green,(604,36,int(173*B),9));pygame.draw.rect(A.window_surface,Colors.lightgreen,(607,34,int(173*B)-3,2));pygame.draw.rect(A.window_surface,Colors.darkgreen,(607,45,int(173*B)-3,3))
	def show_lose_percentage(A,percentage):B=percentage;A.window_surface.blit(A.empty_bar,(600,50));pygame.draw.rect(A.window_surface,Colors.red,(604,56,int(173*B),9));pygame.draw.rect(A.window_surface,Colors.lightred,(607,54,int(173*B)-3,2));pygame.draw.rect(A.window_surface,Colors.darkred,(607,65,int(173*B)-3,3))