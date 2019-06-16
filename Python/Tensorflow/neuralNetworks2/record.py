import os, uuid
import argparse 
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *


# Make sure we can record
try:
	os.mkdir('recording')
except:
	pass

prevAngle = 0

def getAction (state, okSave, prevAngle):
	A = 0
	angleUsed = 0.0
	if (abs(state['angle'] - prevAngle) > 1):
		angleUsed = prevAngle
	else:
		angleUsed = state['angle']

	if (state['wrongway'] or state['speed'] == 0 and okSave):
		return 64, False

	if (state['speed'] < 20):
		A += 4
	if (state['distance_to_center'] >= 1 and angleUsed > -0.1):
		A += 1
	else:
		if (state['distance_to_center'] <= -2 and angleUsed < 0.1):
			A += 2

	return A, okSave 

T = Kart('lighthouse', 500, 500)
good_tries = 0


for tries in range(100):
	# Find a new recording file
	for i in range(100):
		filename = os.path.join('recording',str(uuid.uuid4()))
		if not os.path.isfile(filename):
			break
	
	# Open the recording and write the level name
	f = open(filename, 'w')
	#print(os.path.relpath('lighthouse'), file=f)

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

	while True:
		prevAngle = state['angle']
		A, okSave = getAction(state, okSave, prevAngle)
		state, obs = T.step(A)
		try:
			state, obs = T.step(A)
		except TypeError as e:
			print("TypeError")
			break
		

		if (state['speed'] > 0.5):
			okSave = True
		pause(0.01)	
	
		print( A, state['position_along_track'], state['distance_to_center'], state['angle'], file=f )
		f.flush()
		count += 1

	f.close()
	
	if state['finish_time']:
		print( "Level complete, you're done!" )
		break
	