import os, uuid
import argparse 
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *
import getch
# install from wget https://pypi.python.org/packages/cc/a4/c696c05e0ff9d05b1886cb0210101083db7d330ff964a6d7cd98ad2b2064/getch-1.0.tar.gz#md5=57519f64807285bdfff8e7b62844d3ef
# or from https://pypi.python.org/pypi/getch

# Make sure we can record
try:
	os.mkdir('recording')
except:
	pass

T = Kart('lighthouse', 500, 500)

for tries in range(100):
	# Find a new recording file
	for i in range(100):
		filename = os.path.join('recording',str(uuid.uuid4()))
		if not os.path.isfile(filename):
			break
	
	# Open the recording and write the level name
	f = open(filename, 'w')

	# Restart tux
	T.restart()
	if not T.waitRunning():
		exit(0)

	# Start recording
	#state = {'position':0, 'is_winning': 0}
	print("Begin")
	pause(0.25)
	count = 0
	state, obs = T.step(4)
	okSave = False
	map = {'w':4, 'a':5, 'd':6}

	while True:
		A = map[getch.getch()]
		if not A
			A = 4
		state, obs = T.step(A)
		try:
			state, obs = T.step(A)
		except TypeError as e:
			print("TypeError")
			break
		#pause(10)	s
	
		print( A, state['position_along_track'], state['distance_to_center'], state['angle'], file=f )
		f.flush()

	f.close()
	
	if state['finish_time']:
		print( "Level complete, you're done!" )
		break
	