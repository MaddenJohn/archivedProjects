from pykart import Kart
from time import sleep, time
from random import random
from pylab import *

t0 = time()
K = Kart("lighthouse", 500, 500)
t1 = time()
K.restart()
t2 = time()
print( K.waitRunning() )
t3 = time()
print( K.running, t1-t0, t2-t1, t3-t2 )

im, lbl = None, None
fwd, left, right = 1, 0, 0

#STATE_VARS = ['wrongway', 'finish_time', 'position_along_track', 'position_in_race', 'speed', 'distance_to_center']
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

pause(0.25)
state, obs = K.step(4)
okSave = False

for i in range(10000):
	prevAngle = state['angle']
	# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
	# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)
	testAction = 0
	A = testAction
	A, okSave = getAction(state, okSave, prevAngle)
	print ("Act: " + str(A) +" Dis: "  + str(state['distance_to_center']) + " Ang: " + str(state['angle']))
	state, obs = K.step(A)

	if (state['speed'] > 0.5):
			okSave = True

	ion()
	#figure()
	#subplot(1,2,1)
	if obs is not None:
		if im is None:
			im = imshow(obs)
		else:
			im.set_data(obs)
	draw()
	pause(0.001)
