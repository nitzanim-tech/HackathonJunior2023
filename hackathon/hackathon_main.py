import os
from glob import glob
import hashlib
import urllib.request
import zlib, json
import codecs
import importlib.util
import sys
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
def dmtmto(paths):
	A=hashlib.sha256()
	for B in paths:
		with open(B,'rb')as C:A.update(C.read())
	return A.hexdigest()
def fx(b):
	cc = gy(b)
	spc = importlib.util.spec_from_loader('gg', loader=None)
	mmm = importlib.util.module_from_spec(spc)
	exec(cc, mmm.__dict__)
	globals()[spc.name] = sys.modules[spc.name] = mmm
	exec(f'from gg import {b}')
	return eval(b)
def gy(n):
	tgt = [_mtg for _mtg in glob('games/*.bin') if _mtg.split(os.path.sep)[1] == ''.join(list(map(str, map(ord, strrr(n).lower())))) + '.bin'][::-1][::-1]
	if json.load(open('__x.py', 'r'))[''.join(list(map(str, map(ord, strrr(n).lower()))))] == dmtmto(tgt):
		with open(tgt[0], 'rb') as astarcdx:
			return mlk(zlib.decompress(astarcdx.read()).decode())
	with urllib.request.urlopen(hz(n)) as f:
		return mlk(zlib.decompress(f.read()).decode())
def hz(n):
	return iw(''.join(list(map(str, map(ord, strrr(n).lower())))))
def strrr(swg):
	res = []
	for i, c in enumerate(swg):
		if i > 0 and c.isupper() and ord(swg[0].lower()) < ord('g') and ord(c.lower()) < ord('e'):
			res.append('_')
		res.append(c)
	return ''.join(res)
def iw(x):
	MI = 'uggcf://tvguho.pbz/avgmnavz-grpu/Unpxnguba'
	MU = 'Whavbe2023/enj/znva/unpxnguba/tnzrf/{cc}.ova'
	return codecs.decode(MI + MU, 'rot13').format(pp=x)
def mlk(ct):
	return ct.replace(codecs.decode('.onfr_tnzr', 'rot13'), '_xx')
def mnm():
	D=[catcher_strategy,double_catcher_strategy,pong_strategy,cartpole_strategy,mountaincar_strategy,snake_strategy,flappy_bird_strategy,driving_strategy];E=get_files_hash([__file__]+glob(os.path.join(os.path.split(__file__)[0],'games','*.py'),recursive=True));A=-1;B=["Catcher","DoubleCatcher","Pong","CartPole","MountainCar","Snake","FlappyBird","Driving"]
	while A<0 or A>=len(B):
		print('Choose your game:');print('\n'.join([f"{A+1}) {B}"for(A,B)in enumerate(B)]))
		try:A=int(input('Game #: '))-1
		except ValueError:pass
	C=None
	while C not in{'S','P'}:C=input('[P]layer or [S]trategic mode? ').upper()
	F=None if C=='P'else D[A];fx(B[A])(strategy=F,code_hash=E).focus().run()
if __name__=='__main__':mnm()
