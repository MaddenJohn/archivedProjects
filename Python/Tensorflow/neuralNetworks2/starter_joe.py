import numpy as np
import tensorflow as tf
import util
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *

WH = 600
WW = 800

K = Kart("lighthouse", WW, WH)
K.restart()
print( K.waitRunning() )
# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)

# position in race, position along track
STATE_VARS = ['position_in_race', 'position_along_track', 'speed', 'wrongway', 'finish_time']
#STATE_VARS = ['wrongway', 'finish_time', 'position_along_track', 'position_in_race', 
#	      'speed', 'distance_to_center','angle']

SCORE_WEIGHT = [2, 1.5, 1,-10000, 100000] 
#SCORE_WEIGHT = [-10, 10000, 10, -2, 
#		0.1, -2, 0.0]

#VALID_ACTIONS = [5, 6, 21, 22, 133, 134]
VALID_ACTIONS = [4, 5, 6, 20,132,37,38]

PRWD = 0 # reward based on position on track
ARWD = 0
CRWD = 0
RANK_MODS = 0
dataset = []
loaded = False
states = []
fwd, left, right = 1, 0, 0
wwstep = 0
# Load in previous graph!?
def play_level(policy, K, max_idle_step=70, **kwargs):
	global fwd, left, right, RANK_MODS, PRWD, ARWD, CRWD, TANG, TCEN, states, wwstep
	lpos = 0.0
	cpos = 0.0
	pos_d = 0.0
	PRWD = 0
	ARWD = 0
	CRWD = 0
	wwstep = 0
	K.restart()
	if not K.waitRunning():
		return None

	state, obs = K.step(4*fwd + 1 * left + 2 * right)
	left = -state['angle'] + 0.1*state['distance_to_center'] > .1# or state['distance_to_center'] > 0.2
	right = -state['angle'] + 0.1*state['distance_to_center'] < -.1# or state['distance_to_center'] < -0.2
	fwd = 1
	if abs(state['angle']) > 0.4:
		fwd = np.random() > 0.5

	#print (time())
	pause(2.5)
	#print (time())
	#print ("state", state)
	#Is = [1*obs['image']]
	Is = [obs]
	Ss = [[state[s] for s in STATE_VARS]]
	#print (Ss)
	As = []
	intpos = 0
	im, lbl = None, None
	best_progress, idle_step = 0, 0
	idle_step += 1

	while idle_step < max_idle_step and not state['finish_time'] and wwstep < 11:
		intpos = int(round(state['position_along_track']*1000)) 
		states.append([state[s] for s in STATE_VARS])
		if state['wrongway']:
			wwstep += 1
		else:
			wwstep -= 1
			wwstep = max(wwstep,0)
		if intpos > 105 and intpos <= 117 and idle_step > 25:
			PRWD -= 100
		if abs(state['angle']) < 0.4 and state['speed'] > 0.0 and not state['wrongway']:
			ARWD += 2
		if abs(state['distance_to_center']) < 5.0 and state['speed'] > 0.0 and not state['wrongway']:
			CRWD += 2
		if wwstep >= 10:
			PRWD = -10000
		elif idle_step <= 25:
			PRWD += state['position_along_track']*100
		lpos = cpos
		cpos = state['position_along_track']*100.0
		pos_d = abs(cpos-lpos)

		A = policy(np.concatenate(([Is[0]]*3+Is)[-4:],axis=2), **kwargs)
		#print ("Action", A, idle_step)
		As.append(A)
		
		try:
			state, obs = K.step(int(A))
		except TypeError:
			print ("TypeError")
			print (state, obs)
			break
		#Is.append(1*obs['image'])
		Is.append(obs)
		Ss.append([state[s] for s in STATE_VARS])

		idle_step += 1
		ARWD -= 1
		CRWD -= 1
		if best_progress < state['position_along_track'] and state['speed'] > .2 and not state['wrongway']:
			#print (best_progress, state['position_along_track'], state['speed'])
			best_progress = state['position_along_track']
			idle_step = 0
		#ion()
		#figure()
		#subplot(1,2,1)
		#if obs is not None:
		#	if im is None:
		#		im = imshow(obs)
		#	else:
		#		im.set_data(obs)
		#draw()
		#pause(0.001)
		#print (state['finish_time'])
	while len(As) < len(Is):
		As.append(0)
	return np.array(Is), np.array(Ss), np.array(As)

def play_levels(policy, **kwargs):
	r = []
	r.append( play_level(policy, K, **kwargs) )
	return r

def score_policy(policy, **kwargs):
	score = []
	for i,s,a in play_levels(policy, **kwargs):
		score.append(s[-1])
	return np.mean(score, axis=0)

# Let's now train our own neural policy
sess = tf.Session()

#Try to load pre-existing file
import os.path
if os.path.exists('./assignmentFinal.dat'):
	load('./assignmentFinal.tfg', None, sess)

class CNNPolicy:

	# Only ever create one single CNNPolicy network per graph, otherwise things will FAIL!
	def __init__(self):
		global states
		self.I = tf.placeholder(tf.uint8, (None,WH,WW,12), name='input')
		self.S = tf.placeholder(tf.float32, (None, len(STATE_VARS)), name='input_state')
		
		white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.
		#self.S = tf.convert_to_tensor(states)
		h = white_image
		# TODO: Define your convnet
		# You don't need an auxiliary auto-encoder loss, just create
		# a few encoding conv layers.
		#h = tf.contrib.layers.conv2d(h, 19, (5,5), stride=2, scope="conv1")
		#h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2")
		#h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3")
		#h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4")
		#h = tf.contrib.layers.conv2d(d, len(VALID_ACTIONS), (1,1), stride=2, activation_fn=None, scope="conv5")

		outs = [16, 32, 64, 128, 256]
		for i in range(len(outs)):
			h = tf.contrib.layers.conv2d(h, outs[i], (3,3), stride=2, scope='conv%d'%(i))
			h = tf.contrib.layers.fully_connected(h, int(outs[i]/2.0))

		h = tf.contrib.layers.flatten(h)
		#h = tf.concat([tf.reshape(h,[-1,5]),self.S],0)
		# Hook up a fully connected layer to predict the action
		action_logit = tf.contrib.layers.fully_connected(h, len(VALID_ACTIONS), activation_fn=None)

		self.action_logit = action_logit # This should be a (None,6) tensor
		#action_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=action_logit, labels=action))
		self.predicted_action = tf.identity(tf.argmax(self.action_logit, axis=1), name='action')
		self.variables =  tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
		self.__vars_ph = [tf.placeholder(tf.float32, v.get_shape()) for v in self.variables]
		self.__assign = [v.assign(p) for v,p in zip(self.variables, self.__vars_ph)]
	
	def __call__(self, I, greedy_eps=1e-5, verbose=False):
		global states
		PA = sess.run(self.predicted_action, {self.I: I[None], self.S: [s for s in states]})[0]
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
SAMPLES_PER_EPOCH = 20
EPOCHS = 5
SURVIVAL_RATE = 0.1
VARIANCE_EPS = 0.01
SQUASH = 0.01

mean = np.zeros(P.flat_weights.shape)
std = 0*mean + 1
if os.path.exists('./data.dat') and not loaded:
	with open('data.dat') as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	
	for con in content:
		dataset.append(np.array([float(c) for c in con.split('|')]))
	dataset = np.array(dataset)
	mean = np.mean(dataset, axis=0)
	std = np.std(dataset, axis=0)
	loaded = True

# f(x) evaluates how well a certain parameter setting works
def f(x):
	P.flat_weights = x
	return np.sum(score_policy(P)*SCORE_WEIGHT)

# TODO: Use whichever optimization algorithm you want here
#Cross entropy
def crossEntropyMethod(src = []):
	global RANK_MODS, PRWD, ARWD, CRWD, states
	cemDataset = []
	#sample: theta ~ N(mean, std)
	samples = []
	#print (mean, std)
	if(len(src)):
		#print('\033[94m'+str(src)+'\033[0;0m')
		for i in range(SAMPLES_PER_EPOCH-1):
			sam = np.random.normal(loc=mean,scale=std)
			sam = np.vstack((sam,src))
			sam = np.mean(sam, axis=0)
			samples.append(np.array(sam))
		samples.append(np.array(src[:]))
	else:	 
		for x in range(SAMPLES_PER_EPOCH):
			samples.append(np.random.normal(loc=mean, scale=std))
	#compute reward: f(x)
	scores = []
	count = 1
	for s in samples:
		states = []
		score = f(s)
		score += PRWD
		score += ARWD
		score += CRWD
		scores.append(score)
		print ("sample: " + str(count) + " " + str(score)+" ")
		count += 1
	sortedIndexs = np.argsort(scores)
	sortedIndexs = sortedIndexs[-int(SAMPLES_PER_EPOCH*SURVIVAL_RATE):]
	#print(scores)
	print('\033[93m'+'Best Score: ' + str(scores[sortedIndexs[-1]])+'\033[0;0m\n')
	for i in sortedIndexs:
		cemDataset.append(samples[i]) 	
	#select top p%: (survival rate)
	#fit Gaussian for new mean, std
	return cemDataset

#repeat
for epoch in range(EPOCHS):
	print('\033[92m'+'Epoch: ' + str(epoch)+'\033[0;0m')
	if(len(dataset)):
		dataset = crossEntropyMethod(np.mean(dataset, axis=0)[:])
	else:
		dataset = crossEntropyMethod()
	mean = np.mean(dataset, axis=0)
	std = np.std(dataset, axis=0)
best_policies = dataset
# To save the intermediate result use
P.flat_weights = best_policies[-1]
util.save('assignmentFinal.tfg', session=sess)

f = open('./data.dat','w')
# write our top policies to read in for next time
for b in best_policies:
	fline = ''
	for d in b:
		fline+=str(d)+'|'
	fline = fline[:-1]+'\n'
	f.write(fline)

P.flat_weights = best_policies[-1]

#pause(0.01)
big_kart = Kart("lighthouse", WW, WH)
big_kart.restart()
if not big_kart.waitRunning():
	exit(1)
big_kart.step(0)

def step(I):
	A = P(I, verbose=True)
	#print (str(A))
	big_kart.step(A)
	return A

play_level(step, K)
