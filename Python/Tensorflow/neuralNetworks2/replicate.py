import numpy as np
import tensorflow as tf
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *

K = Kart("lighthouse", 500, 500)
K.restart()
print( K.waitRunning() )
# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)

# position in race, position along track
#STATE_VARS = ['position_in_race', 'position_along_track', 'speed', 'wrongway', 'finish_time']
STATE_VARS = ['wrongway', 'finish_time', 'position_along_track', 'speed', 'distance_to_center']

#SCORE_WEIGHT = [0.1, 0.01, 0.05, -1] 
#            place 
# -10 1 0.5 -1 0.001 -10 
SCORE_WEIGHT = [-200, 1000000000000, 500, 0.001, -5]

VALID_ACTIONS = [5, 6, 20, 21, 22, 132, 133, 134] #8?
#VALID_ACTIONS = [4, 5, 6]

# function to help AI in decision making. This is just for cases when we
# want to progress farther. Right now this i able to complete the track, 3 times in a row
# check the implementation in main.py for an implementation that finishes much fast
# in roughly 4 minutes total for all 3 laps 
def specialCases(A, state, okSave, idle_step):
	originalA = A
	A = 0
	original = False
	if (state['wrongway'] or state['speed'] == 0 and okSave):
				A = 64
				okSave = False
	else: 
		#if ((abs(state['distance_to_center'])) < 3 and abs(state['angle']) < 0.2):
		#	A = 4
		#else :
		if (state['speed'] > 100):
			A = 8
		else: 
			if (abs(state['distance_to_center']) < 5):
				if (state['angle'] > 0.3):
					A = 5
				if (state['angle'] < -0.3):
					A = 6
			else:
				if (state['distance_to_center'] >= 5):
					A = 5
					#if (state['angle'] < -1):
					#	A = 4
				else:
					A = 6
					#if (state['angle'] > 1):
					#	A = 4
	print ("OA: ", originalA,  "A", A, "st", idle_step, "spd", state['speed'], "Ang", state['angle'])
	if (A == 0):
		A = originalA
		original = True
	return A, okSave, original

def play_level(policy, K, max_idle_step=200, **kwargs):
	K.restart()
	if not K.waitRunning():
		return None
	
	state, obs = K.step(0)
	pause(2.4)
	Is = [obs]
	Ss = [[state[s] for s in STATE_VARS]]
	As = []
	im, lbl = None, None
	best_progress, idle_step = 0, 0
	okSave = False
	total_Original = 0.0
	total_steps = 0.0
	while idle_step < max_idle_step and not state['finish_time']:
		#A = 4
		A = policy(np.concatenate(([Is[0]]*3+Is)[-4:],axis=2), **kwargs)
		As.append(A)
		A, okSave, original = specialCases(A, state, okSave, idle_step)
		if (original):
			total_Original += 1
		try:
			state, obs = K.step(int(A))
		except TypeError:
			print ("TypeError")
			break
		Is.append(obs)
		Ss.append([state[s] for s in STATE_VARS])
		Ss[-1][-1] = abs(Ss[-1][-1])
		if (state['speed'] > 0.5):
			okSave = True

		idle_step += 1
		if best_progress < state['position_along_track'] and state['speed'] > 0.1:
			#print ("BestProg: ", best_progress, " CurProg: ", state['position_along_track'], " Spd: ",state['speed'])
			best_progress = state['position_along_track']
			idle_step = 0
			#okSave = True
		ion()
		#figure()
		#subplot(1,2,1)
		if obs is not None:
			if im is None:
				im = imshow(obs)
			else:
				im.set_data(obs)
		draw()
		#pause(0.001)
		total_steps += 1
		#print (state['finish_time'])
		print ("AI percent: ", str(total_Original / total_steps), "dist: ", state['position_along_track'])
	while len(As) < len(Is):
		As.append(0)
	
	return np.array(Is), np.array(Ss), np.array(As)

def play_levels(policy, **kwargs):
	r = []
	r.append( play_level(policy, K, **kwargs) )
	#print (r)
	return r

def score_policy(policy, **kwargs):
	score = []
	for i,s,a in play_levels(policy, **kwargs):
		score.append(s[-1])
		#print (s)
	print (STATE_VARS)
	print (SCORE_WEIGHT)
	print (np.mean(score, axis=0))
	return np.mean(score, axis=0)

# Let's now train our own neural policy
sess = tf.Session()

class CNNPolicy:
	# Only ever create one single CNNPolicy network per graph, otherwise things will FAIL!
	def __init__(self):
		self.I = tf.placeholder(tf.uint8, (None,500,500,12), name='input')
		
		white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.
		h = white_image
		# TODO: Define your convnet
		# You don't need an auxiliary auto-encoder loss, just create
		# a few encoding conv layers.
		for i, n in enumerate([10,20,30,40,50,60]):
			h = tf.contrib.layers.conv2d(h, 20, (3,3), stride=2, scope='conv%d'%(i))
		h = tf.contrib.layers.flatten(h)
		# Hook up a fully connected layer to predict the action
		action_logit = tf.contrib.layers.fully_connected(h, len(VALID_ACTIONS), activation_fn=None)

		self.action_logit = action_logit # This should be a (None,6) tensor
		#action_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=action_logit, labels=action))
		self.predicted_action = tf.identity(tf.argmax(self.action_logit, axis=1), name='action')
		self.variables =  tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
		self.__vars_ph = [tf.placeholder(tf.float32, v.get_shape()) for v in self.variables]
		self.__assign = [v.assign(p) for v,p in zip(self.variables, self.__vars_ph)]
	
	def __call__(self, I, greedy_eps=1e-5, verbose=False):
		PA = sess.run(self.predicted_action, {self.I: I[None]})[0]
		
		return VALID_ACTIONS[int(PA)]
	
	@property
	def flat_weights(self):
		import numpy as np
		W = self.weights
		return np.concatenate([w.flat for w in W])
	
	@flat_weights.setter
	def flat_weights(self, w):
		import numpy as np
		S = [v.get_shape().as_list() for v in self.variables]
		s = [np.prod(i) for i in S]
		O = [0] + list(np.cumsum(s))
		assert O[-1] <= w.size
		W = [w[O[i]:O[i+1]].reshape(S[i]) for i in range(len(S))]
		self.weights = W
	
	@property
	def weights(self):
		return sess.run(self.variables)
	
	@weights.setter
	def weights(self, weights):
		sess.run(self.__assign, {v:w for v,w in zip(self.__vars_ph, weights)})

# Define your CNN policy
P = CNNPolicy()

# Initialize the variables
sess.run(tf.global_variables_initializer())

# Let's start training
# you might find these parameters useful, or not ;)
SAMPLES_PER_EPOCH = 10
EPOCHS = 3
SURVIVAL_RATE = 0.2
VARIANCE_EPS = 0.01

mean = np.zeros(P.flat_weights.shape)
std = 0*mean + 1

# f(x) evaluates how well a certain parameter setting works
def f(x):
	P.flat_weights = x
	return np.sum(score_policy(P)*SCORE_WEIGHT)

# TODO: Use whichever optimization algorithm you want here
#Cross entropy
def crossEntropyMethod():
	cemDataset = []
	#sample: theta ~ N(mean, std)
	samples = []
	#print (mean, std)
	for x in range(SAMPLES_PER_EPOCH):
		samples.append(np.random.normal(loc=mean, scale=std))
	#compute reward: f(x)
	scores = []
	count = 1
	for s in samples:
		score = f(s)
		scores.append(score)
		print ("sample: " + str(count) + " " + str(score))
		count += 1
	sortedIndexs = np.argsort(scores)
	sortedIndexs = sortedIndexs[-int(SAMPLES_PER_EPOCH*SURVIVAL_RATE):]
	#print(scores)
	print('Best Score: ' + str(scores[sortedIndexs[-1]]))
	for i in sortedIndexs:
		cemDataset.append(samples[i]) 	
	#select top p%: (survival rate)
	#fit Gaussian for new mean, std
	return cemDataset

#repeat
dataset = []
for epoch in range(EPOCHS):
	print('Epoch: ' + str(epoch))
	dataset = crossEntropyMethod() 
	mean = np.mean(dataset, axis=0)
	std = np.std(dataset, axis=0)
best_policies = dataset

# To save the intermediate result use
P.flat_weights = best_policies[-1]
util.save('assignmentFinal.tfg', session=sess)

P.flat_weights = best_policies[-1]

#pause(0.01)
big_kart = Kart("lighthouse", 500, 500)
big_kart.restart()
if not big_kart.waitRunning():
	exit(1)
big_kart.step(0)

def step(I):
	A = P(I, verbose=True)
	print (str(A))
	big_kart.step(A)
	return A

play_level(step, K)
