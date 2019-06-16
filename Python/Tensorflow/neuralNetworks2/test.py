import os.path
from pykart import Kart
from time import sleep, time
from random import random
import numpy as np
import tensorflow as tf
import util 
from pylab import *

size = 300
K = Kart("lighthouse", size, size)
STATE_VARS = ['position_along_track', 'wrongway', 'distance_to_center', 'angle', 'speed']
SCORE_WEIGHT = [1, -1, -0.5, 0, 0.1]
LOSS_WEIGHT = SCORE_WEIGHT
VALID_ACTIONS = [4, 5, 6]
epochCount = 10
verbose = False
greedy_eps = 0.2

def getFromTFG(obs, state, *kwargs):
	#PS = sess.run(self.predicted_state, {self.I: [I], self.S: [state]})[0]
	PS = sess.run(pred_state, {in_img: [obs], in_state: [state]})[0]
	PS = [PS[0:5],PS[5:10],PS[10:15]]
	action_score = np.dot(np.abs(PS), SCORE_WEIGHT)
	if verbose:
		print( PS )
		print( action_score )
	
	# Add some epsilon greedy exploration
	action_score += np.random.normal(0,1,len(VALID_ACTIONS)) * (np.random.random(len(VALID_ACTIONS)) < greedy_eps)
	return VALID_ACTIONS[int(np.argmax(action_score))]




def specialCase (state, okSave, A, idle_step):
	if not (okSave):
		return 4, False
	if (state['speed'] > 50):
		return A-4, okSave
	if ((state['wrongway'] or state['speed'] < 1) and okSave and state['position_along_track'] > 0.05):
		return 64, False
	return A, okSave

def safe_step(K, A):
	ret = None
	while ret is None:
		ret = K.step(A)
	return ret

def play_level(K, max_idle_step=300, **kwargs):
	K.restart()
	if not K.waitRunning():
		return None
	
	obs = None
	while obs is None:
		state, obs = safe_step(K, 0)
		
	pause(0.1)
	
	Is = [obs]
	Ss = [[abs(state[s]) for s in STATE_VARS]]
	As = []
	
	best_progress, idle_step = 0, 0
	okSave = False
	while True:
		if (best_progress > 0.5):
			max_idle_step = 300 + (300 * best_progress)
		if obs is None:
			A = 0
		else:
			A = getFromTFG(obs, [state[s] for s in STATE_VARS], **kwargs)
		if (idle_step % 100 == 0 and idle_step > 0):
			print(A, idle_step)
		print (A, state['timestamp'])
		As.append(A)
		if (epochCount > 1):
			A, okSave = specialCase(state, okSave, A, idle_step)
		state, obs = safe_step(K, A)
		Is.append(obs)
		Ss.append([abs(state[s]) for s in STATE_VARS])

		idle_step += 1
		difference = abs(state['position_along_track'] - best_progress)
		#print (difference)
		if best_progress < state['position_along_track'] and state['speed'] > .2 and difference < 0.05:
			#print (best_progress, state['position_along_track'])
			best_progress = state['position_along_track']
			idle_step = 0
		if (state['speed'] > 10):
			okSave = True
		pause (0.01)




sess = tf.Session()

# if os.path.exists(''):
print ("Loading: " + str(sys.argv[1]))
graph = util.load(sys.argv[1], session=sess)
graph = tf.get_default_graph()
print ("Done Load")


#img = tf.placeholder(tf.uint8, (None,size,size,3))
#st = tf.placeholder(tf.float32, (None, len(STATE_VARS)))

# key should be predicted state
pred_state = graph.get_tensor_by_name('predicted_state:0')
in_img = graph.get_tensor_by_name('input_image:0')
in_state = graph.get_tensor_by_name('input_state:0')

#act = graph.get_tensor_by_name('action')
#state_pred = graph.get_tensor_by_name('state_pred')
#label = graph.get_tensor_by_name('label')



play_level(K)


