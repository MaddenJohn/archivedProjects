from pykart import Kart
from time import sleep, time
from random import random
import numpy as np
import tensorflow as tf
import util

#t0 = time()
K = Kart("lighthouse", 300, 200)
#t1 = time()
#K.restart()
#t2 = time()
#print( K.waitRunning() )
#t3 = time()
#print( K.running, t1-t0, t2-t1, t3-t2 )

STATE_VARS = ['position_along_track', 'wrongway', 'distance_to_center', 'angle', 'speed']
SCORE_WEIGHT = [1, -1, -.5, 0, .1]

# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)
VALID_ACTIONS = [4, 5, 6]

def safe_step(K, A):
	ret = None
	while ret is None:
		ret = K.step(A)
	return ret

num_saved = 0

def play_level(policy, K, max_idle_step=300, **kwargs):
	K.restart()
	if not K.waitRunning():
		return None
	
	obs = None
	while obs is None:
		state, obs = safe_step(K, 0)
		
	sleep(2.2)
	
	Is = [obs]
	Ss = [[state[s] for s in STATE_VARS]]
	As = []
	
	global num_saved
	best_progress, idle_step = -1, 0
	while idle_step < max_idle_step:
		if obs is None:
			A = 0
		else:
			A = policy(obs, [state[s] for s in STATE_VARS], **kwargs)
		print(A)
		As.append(A)
		
		state, obs = safe_step(K, A)
		Is.append(obs)
		Ss.append([state[s] for s in STATE_VARS])

		idle_step += 1
		if best_progress < state['position_along_track'] and state['speed'] > .2:
			print (best_progress, state['position_along_track'])
			best_progress = state['position_along_track']
			idle_step = 0
		sleep(0.01)
	while len(As) < len(Is):
		As.append(0)
	if best_progress > .5:
		util.save('assignmentFinal_' + str(num_saved) + '.tfg', session=sess)
		num_saved += 1
	return np.array(Is), np.array(Ss), np.array(As)
	
def play_levels(policy, **kwargs):
	r = []
	r.append( play_level(policy, K, **kwargs) )
	return r

#####################################################
###   Now let's now train our own neural policy   ###
#####################################################
sess = tf.Session()

class CNNPolicy:
	def __init__(self):
		self.I = tf.placeholder(tf.uint8, (None,200,300,3), name='input_image')
		self.S = tf.placeholder(tf.float32, (None,len(STATE_VARS)), name='input_state')
		
		white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.

		########################
		### Your Code Here   ###
		########################
		'''
		h = white_image
		C0 = 15
		D = 3
		S = 4
		for i in range(D):
			h = tf.contrib.layers.conv2d(h, int(C0*1.5**i), (3,3), stride=S, scope='conv%d'%(i), weights_regularizer=tf.nn.l2_loss)
		h = tf.contrib.layers.fully_connected(h, 20);
		for i in range(D - 1)[::-1]:
		  h = tf.contrib.layers.conv2d_transpose(h, int(C0*1.5**i), (3,3), stride=S, scope='upconv%d'%(i), weights_regularizer=tf.nn.l2_loss)
			
		h = tf.contrib.layers.conv2d(h, 3, (1,1), weights_regularizer=tf.nn.l2_loss)
		
		h = tf.contrib.layers.flatten(h)
		h = tf.concat([h, self.S], -1)
		'''
		h = self.S
		h = tf.contrib.layers.fully_connected(h, 30);
		h = tf.contrib.layers.fully_connected(h, 60);
		h = tf.contrib.layers.fully_connected(h, 90);
		
		predicted_state = tf.contrib.layers.fully_connected(h, len(VALID_ACTIONS) * len(STATE_VARS), activation_fn=None);
		
		predicted_state = tf.identity(predicted_state, name='predicted_state')
		print(predicted_state)
		self.predicted_state = tf.reshape(predicted_state, (-1, len(VALID_ACTIONS), len(STATE_VARS)))
		print(self.predicted_state)

		self.action = tf.placeholder(tf.int32, (None,), name='action') # action that was taken during game-play
		indices = tf.stack([tf.range(tf.size(self.action)), self.action], axis=1)
		self.action_conditioned_state = tf.gather_nd( self.predicted_state, indices, name='state_pred')
		self.label = tf.placeholder(tf.float32, (None,len(STATE_VARS)), name='label')

		self.action_loss = tf.reduce_sum(np.abs(SCORE_WEIGHT) * (self.label - self.action_conditioned_state)**2)

		self.loss = self.action_loss
		
		optimizer = tf.train.AdamOptimizer(0.001, 0.9, 0.999)
		self.train = optimizer.minimize(self.loss)

		print( "Total number of variables used ", np.sum([v.get_shape().num_elements() for v in tf.trainable_variables()]) )
	
	''' This function returns an action to take based on our policy and 
		the given input image.  With probability greedy_eps the policy will
		return a random action. '''
	def __call__(self, I, state, greedy_eps=1e-5, verbose=False):
		PS = sess.run(self.predicted_state, {self.I: [I], self.S: [state]})[0]
		
		action_score = np.dot(np.abs(PS), SCORE_WEIGHT)
		if verbose:
			print( PS )
			print( action_score )
		
		# Add some epsilon greedy exploration
		action_score += np.random.normal(0,1,len(VALID_ACTIONS)) * (np.random.random(len(VALID_ACTIONS)) < greedy_eps)
		return VALID_ACTIONS[int(np.argmax(action_score))]

# Define your CNN policy
P = CNNPolicy()

# Initialize the variables
sess.run(tf.global_variables_initializer())

################################
###   Let's start training   ###
################################
SAMPLES_PER_LEVEL = 1000
BS = 64
TRAIN_ITER_PER_EPOCH = 100
MAX_DATASET_SIZE = 10000

best_policies = []
best_score = -1

dataset = []
for epoch in range(100):
	print('%d:'%(epoch))
	# Let's collect some data
	eps = 0.2
	if ((epoch % 5) == 0):
		eps = 0
	data = play_levels(P,greedy_eps=eps)
	print( np.mean([s[-1] for i,s,a in data], axis=0) )
	
	if len(data[0]) == 1:
	  continue
	
	for Is, Ss, As in data:
		samples = np.random.choice(len(Is)-1, size=SAMPLES_PER_LEVEL)
		for s in samples:
			I = Is[s]
			A = As[s]
			# Predict the delta in state
			future_state = np.mean(Ss[s+1:s+11], axis=0)-Ss[s]
			current_state = Ss[s]
			dataset.append( (I, future_state, A, current_state) )
	
	# Trim the dataset and shuffle
	dataset = dataset[-MAX_DATASET_SIZE//2:]
	np.random.shuffle(dataset)
	
	# Train the network a bunch
	for it in range(TRAIN_ITER_PER_EPOCH):
		batch_data = [dataset[i] for i in np.random.choice(len(dataset), BS)]
		images = np.stack([I for I,F,A,C in batch_data], axis=0)
		future_state = np.stack([F for I,F,A,C in batch_data], axis=0)
		actions = np.stack([VALID_ACTIONS.index(A) for I,F,A,C in batch_data], axis=0)
		current_state = np.stack([C for I,F,A,C in batch_data], axis=0)
		
		loss, _ = sess.run( [P.loss, P.train], {P.I: images, P.action: actions, P.label: future_state, P.S: current_state} )
print( loss )