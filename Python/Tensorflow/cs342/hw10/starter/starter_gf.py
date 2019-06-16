"""
This assignment requires pytux, make sure to download a binary or compile it from source. Then link (or copy) the pytux and data directory here
ln -s /path/to/supertux/pytux pytux 
ln -s /path/to/supertux/data data

It is also recommended that you launch the training script from an actual lab machine, not through ssh (off-screen rendering is strictly speaking implemented, but the nvidia driver can be moody and might decide not to render an image).
"""
import numpy as np
import tensorflow as tf
import pytux
import util

levels = ["data/levels/world1/01 - Welcome to Antarctica.stl", "data/levels/world1/02 - The Journey Begins.stl", "data/levels/world1/03 - Via Nostalgica.stl", "data/levels/world1/04 - Tobgle Road.stl", "data/levels/world1/05 - The Somewhat Smaller Bath.stl"]

tuxs = [pytux.Tux(l, 64, 64, acting=True, visible=True, synchronized=True) for l in levels]
STATE_VARS = ['position', 'coins', 'is_dying']

SCORE_WEIGHT = [1, 0, -0.1] # Score different things while playing (progress through the level, #coins, death)

# List of valid actions (1: left, 2: right, 16: jump, and all valid combinations). We ignore up and down for now.
VALID_ACTIONS = [0, 1, 2, 16, 17, 18]

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
		
		try:
			fid, act, state, obs = T.step(A)
		except TypeError:
			break
		Is.append(1*obs['image'])
		Ss.append([state[s] for s in STATE_VARS])

		idle_step += 1
		if best_progress < state['position']:
			best_progress = state['position']
			idle_step = 0
	while len(As) < len(Is):
		As.append(0)
	return np.array(Is), np.array(Ss), np.array(As)

def play_levels(policy, **kwargs):
	r = []
	for T in tuxs:
		r.append( play_level(policy, T, **kwargs) )
	return r

def score_policy(policy, **kwargs):
	score = []
	for i,s,a in play_levels(policy, **kwargs):
		score.append(s[-1])
	return np.mean(score, axis=0)

# Let's now train our own neural policy
sess = tf.Session()

class CNNPolicy:
	# Only ever create one single CNNPolicy network per graph, otherwise things will FAIL!
	def __init__(self):
		self.I = tf.placeholder(tf.uint8, (None,64,64,4*3), name='input')
		
		white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.
		h = white_image
		# TODO: Define your convnet
		# You don't need an auxiliary auto-encoder loss, just create
		# a few encoding conv layers.
		for i, n in enumerate([10,20,30,40,50,60]):
			h = tf.contrib.layers.conv2d(h, 20, (3,3), stride=2, scope='conv%d'%(i))
		h = tf.contrib.layers.flatten(h)
		# Hook up a fully connected layer to predict the action
		action_logit = tf.contrib.layers.fully_connected(h, 6, activation_fn=None)

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
SAMPLES_PER_EPOCH = 50
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
	for s in samples:
		scores.append(f(s))
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
util.save('assignment10_gf.tfg', session=sess)


# Visualize how well tux is doing
P.flat_weights = best_policies[-1]
for l in levels:
	big_tux = pytux.Tux(l, 640, 640, acting=True, visible=True, synchronized=False)
	big_tux.restart()
	if not big_tux.waitRunning():
		exit(1)
	big_tux.step(0)

	def step(I):
		A = P(I, verbose=True)
		big_tux.step(A)
		return A

	play_level(step, tuxs[0])
