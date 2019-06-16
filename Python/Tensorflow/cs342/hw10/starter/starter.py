"""
This assignment required pytux, make sure to download a binary or compile it from source. Then link (or copy) the pytux and data directory here
ln -s /path/to/supertux/pytux pytux 
ln -s /path/to/supertux/data data

It is also recommended that you launch the training script from an actual lab machine, not through ssh (off-screen rendering is strictly speaking implemented, but the nvidia driver can be moody and might decide not to render an image).
"""

#########################
###   Initial Setup   ###
#########################
import numpy as np
import tensorflow as tf
import pytux
import util

try:
	from joblib import Parallel, delayed
except:
	def Parallel(*args,**kwargs): return list
	def delayed(f): return f
#levels = ["data/levels/world1/01 - Welcome to Antarctica.stl"]
levels = ["data/levels/world1/01 - Welcome to Antarctica.stl", "data/levels/world1/02 - The Journey Begins.stl", "data/levels/world1/03 - Via Nostalgica.stl", "data/levels/world1/04 - Tobgle Road.stl", "data/levels/world1/05 - The Somewhat Smaller Bath.stl"]

tuxs = [pytux.Tux(l, 64, 64, acting=True, visible=True, synchronized=True) for l in levels]
STATE_VARS = ['position', 'coins', 'is_dying']

'''
We have to do some reward shaping to get tux to avoid getting stuck in bad policies
	and help it get through the level.

Completing the level and collect 100 coins gives you the same score, dying is worth 20 coins '''
SCORE_WEIGHT = [1, 0.01, -0.01]

# List of valid actions (1: left, 2: right, 16: jump, and all valid combinations). We ignore up and down for now.
VALID_ACTIONS = [0, 1, 2, 16, 17, 18]

###############################################
###   Logic to play tux given some policy   ###
###############################################

''' Uses a given policy to play a level in tux until the level
is either completed, tux dies or a timeout is hit. '''
def play_level(policy, T, max_idle_step=30, **kwargs):
	T.restart()
	if not T.waitRunning():
		return None
	
	fid, act, state, obs = T.step(0)
	
	Is = [1*obs['image']]
	Ss = [[state[s] for s in STATE_VARS]]
	As = []
	
	best_progress, idle_step = 0, 0
	while idle_step < max_idle_step and not state['is_dying']:
		A = policy(np.concatenate(([Is[0]]*3+Is)[-4:],axis=2), **kwargs)
		As.append(A)
		
		fid, act, state, obs = T.step(A)
		Is.append(1*obs['image'])
		Ss.append([state[s] for s in STATE_VARS])
		#print (state)

		idle_step += 1
		if best_progress < state['position']:
			best_progress = state['position']
			idle_step = 0
	while len(As) < len(Is):
		As.append(0)
	return np.array(Is), np.array(Ss), np.array(As)

# Plays all levels
def play_levels(policy, **kwargs):
	r = []
	for T in tuxs:
		r.append( play_level(policy, T, **kwargs) )
	return r

# Scores a given policy by computing the the average scores
# 	across all levels.
def score_policy(policy, **kwargs):
	score = []
	for i,s,a in play_levels(policy, **kwargs):
		score.append(s[-1])
	return np.mean(score, axis=0)

#####################################################
###   Now let's now train our own neural policy   ###
#####################################################
sess = tf.Session()

class CNNPolicy:
	def __init__(self):
		self.I = tf.placeholder(tf.uint8, (None,64,64,4*3), name='input')
		
		white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.
		ae_target = white_image[:,:,:,-3:] # auto-encoder predicts current frame

		########################
		### Your Code Here   ###
		########################

		h = ae_target
		C0 = 5
		D = 5
		hs = []
		#hw7 and hw8 solution, 
		for i in range(D):
			hs.append(h)
			h = tf.contrib.layers.conv2d(h, C0*int(1.5**i), (3,3), stride=2, scope='conv%d'%(i+1))
			h = tf.concat([h, tf.image.resize_images(ae_target,  tf.shape(h)[1:3])], axis=-1) #8
		for i in range(D)[::-1]:
			h = tf.contrib.layers.conv2d_transpose(h, C0*int(1.5**i), (3,3), stride=2, scope='upconv%d'%(i+1))
			h = tf.concat([h, hs[i]], axis=-1)
		h_end = tf.contrib.layers.conv2d(h, C0, (1,1), scope='fc1') #8
		h = tf.contrib.layers.conv2d(h_end, C0, (1,1), stride=2) 
		h = tf.contrib.layers.conv2d(h, C0, (1,1), stride=2) 
		h = tf.contrib.layers.conv2d(h, C0, (1,1), stride=2) 
		h = tf.contrib.layers.conv2d(h, C0, (1,1), stride=2) 
		h1 = tf.contrib.layers.conv2d(h, len(VALID_ACTIONS), (1,1), scope='cls', activation_fn=None)
		ae_prediction = h1
		ae_prediction = tf.contrib.layers.flatten(ae_prediction)
		ae_prediction = tf.contrib.layers.fully_connected(ae_prediction, (len(VALID_ACTIONS)), activation_fn=None)
		ae_prediction = tf.identity(ae_prediction, name='ae_prediction')
		
		d = h_end

		# Let's just grab a small patch to predict
		stacked = tf.concat([d[:,:,:,-3:], white_image[:,:,:,-3:]], axis=-1)
		crop_size = (tf.shape(white_image)[0], 20, 20, 6) # feel free to increase/decrease this size as you see fit
		cropped = tf.random_crop(stacked, crop_size)

		self.ae_loss = tf.reduce_mean((cropped[:,:,:,:3] - cropped[:,:,:,3:]) ** 2)

		predicted_state = h_end
		predicted_state = tf.contrib.layers.conv2d(predicted_state, (len(VALID_ACTIONS) * len(STATE_VARS)), (1,1), activation_fn=None)
		predicted_state = tf.contrib.layers.flatten(predicted_state)
		predicted_state = tf.contrib.layers.fully_connected(predicted_state, (len(VALID_ACTIONS) * len(STATE_VARS)), activation_fn=None)
		

		predicted_state = tf.identity(predicted_state, name='predicted_state')
		self.predicted_state = tf.reshape(predicted_state, (-1, len(VALID_ACTIONS), len(STATE_VARS)))
		#score = np.sum(score_policy(P) * SCORE_WEIGHT)
		self.action = tf.placeholder(tf.int32, (None,), name='action') # action that was taken during game-play
		indices = tf.stack([tf.range(tf.size(self.action)), self.action], axis=1)
		self.action_conditioned_state = tf.gather_nd( self.predicted_state, indices, name='state_pred')
		self.label = tf.placeholder(tf.float32, (None,len(STATE_VARS)), name='label')

		self.action_loss = tf.reduce_sum(np.abs(SCORE_WEIGHT) * (self.label - self.action_conditioned_state)**2)

		# Total loss is a weighted combination of our auto-encoder loss and playing well in the game.
		# Feel free to tweak the weight, this is by no means optimal.
		#self.loss = 0.5 * self.ae_loss + self.action_loss
		#self.loss = 0.001 * self.ae_loss + self.action_loss
		self.loss = 1e-6 * self.ae_loss + self.action_loss

		optimizer = tf.train.AdamOptimizer(0.001, 0.9, 0.999)
		self.train = optimizer.minimize(self.loss)
	
	''' This function returns an action to take based on our policy and 
		the given input image.  With probability greedy_eps the policy will
		return a random action. '''
	def __call__(self, I, greedy_eps=1e-5, verbose=False):
		PS = sess.run(self.predicted_state, {self.I: I[None]})[0]
		
		action_score = np.dot(PS, SCORE_WEIGHT)
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

dataset = []
for epoch in range(100):
	# Let's collect some data
	data = play_levels(P,greedy_eps=0.2)
	print( np.mean([s[-1] for i,s,a in data], axis=0) )
	
	for Is, Ss, As in data:
		samples = np.random.choice(len(Is)-1, size=SAMPLES_PER_LEVEL)
		for s in samples:
			I = Is[max(0,s-3):s+1]
			while len(I) < 4:
				I = np.concatenate( (I[0,None], I), axis=0 )
			A = As[s]
			# Predict the delta in state
			future_state = np.mean(Ss[s+1:s+11], axis=0)-Ss[s]
			dataset.append( (np.concatenate(I, axis=2), future_state, A) )
	
	# Trim the dataset and shuffle
	dataset = dataset[-MAX_DATASET_SIZE//2:]
	np.random.shuffle(dataset)
	
	# Train the network a bunch
	for it in range(TRAIN_ITER_PER_EPOCH):
		batch_data = [dataset[i] for i in np.random.choice(len(dataset), BS)]
		images = np.stack([I for I,F,A in batch_data], axis=0)
		future_state = np.stack([F for I,F,A in batch_data], axis=0)
		actions = np.stack([VALID_ACTIONS.index(A) for I,F,A in batch_data], axis=0)
		
		loss, _ = sess.run( [P.loss, P.train], {P.I: images, P.action: actions, P.label: future_state} )
	print( 'loss: ' , loss )
	score = np.sum(score_policy(P) * SCORE_WEIGHT)
	print( 'score: ' , score)
	if (score > 0.2):
		name = 'assignment10_' + str(int(1000 * score)) + '.tfg'
		util.save(name, session=sess)
	
print( score_policy(P) )

###########################################
###   Visualize how well tux is doing   ###
###########################################
while True:
	ans = input('[Enter] when ready to watch results, anything else to exit.')
	if len(ans) > 0:
		break
	for l in levels:
		big_tux = pytux.Tux(l, 640, 640, acting=True, visible=True, synchronized=False)
		big_tux.restart()
		if not big_tux.waitRunning():
			exit(1)
		big_tux.step(0)

		def step(I):
			A = P(I, verbose=False)
			big_tux.step(A)
			return A

		play_level(step, tuxs[0])

util.save('assignment10.tfg', session=sess)