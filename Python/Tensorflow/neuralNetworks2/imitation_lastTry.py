import numpy as np
import tensorflow as tf
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *
import util

# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)

STATE_VARS = ['position_along_track', 'distance_to_center', 'angle']
SCORE_WEIGHT = [1, -1, -1]
VALID_ACTIONS = [4, 5, 6]
size = 300

K = Kart("lighthouse", size, size)
K.restart()
print( K.waitRunning() )

def parser(dataset_name):
    f = open(dataset_name, 'r')
    lines = f.readlines()
    f.close()
    dataList = {}
    for i, line in enumerate(lines):  
        data = line.split()
        dataList[round(float(data[1]), 3)] = data
    return dataList


def load_dataset(dataset_name):
    return parser(dataset_name)


state = {'position_along_track':0.0, 'angle':0.0, 'distance_to_center':0.0}
A = 4
def play_level(policy, K, max_idle_step=500, **kwargs):
    K.restart()
    if not K.waitRunning():
        return None
    
    state, obs = K.step(0)
    print ("first")
    pause(2.4)
    Is = [obs]
    Ss = [[state[s] for s in STATE_VARS]]
    Ss = [[abs(state[s]) for s in STATE_VARS]]
    As = []
    im, lbl = None, None
    best_progress, idle_step = 0, 0
    okSave = False
    total_Original = 0.0
    total_steps = 0.0
    while idle_step < max_idle_step and not state['finish_time']:
        A = policy(np.concatenate(([Is[0]]*3+Is)[-4:],axis=2), [state[s] for s in STATE_VARS], **kwargs)
        print ("policyAction: ",A, idle_step, state['position_along_track'])
        As.append(A)
        try:
            state, obs = K.step(int(A))
        except TypeError:
            print ("TypeError")
            break
        Is.append(obs)
        #Ss.append([state[s] for s in STATE_VARS])
        Ss.append([abs(state[s]) for s in STATE_VARS])
        Ss[-1][-1] = abs(Ss[-1][-1])
        idle_step += 1
        if best_progress < state['position_along_track'] and state['speed'] > 0.1:
            best_progress = state['position_along_track']
            idle_step = 0
        pause(0.01)
    while len(As) < len(Is):
        As.append(0)
    if (best_progress > 0.75):
        util.save('imitation_last_' + str(best_progress) + '.tfg', session=sess)
    
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
    return np.mean(score, axis=0)

# Let's now train our own neural policy
sess = tf.Session()

class CNNPolicy:
    # Only ever create one single CNNPolicy network per graph, otherwise things will FAIL!
    def __init__(self):
        # need to get this data
        train_data = load_dataset('0cp_new')
        data = []
        for x in range(len(train_data)):
            data.append(x)

        for k in train_data:
            index = abs(int(k*1000))
            data[index] = (k, train_data[k])

        self.I = tf.placeholder(tf.uint8, (None,size,size,3), name='input_image')
        self.S = tf.placeholder(tf.float32, (None, len(STATE_VARS)), name='input_state')
        
        c_position, c_angle, c_center, c_action = round(self.S['position_along_track'], 3), self.S['angle'], self.S['distance_to_center'],  A
        v_action, v_position, v_center, v_angle = int(train_data[current_position][0]), float(train_data[current_position][1]), float(train_data[current_position][2]), float(train_data[current_position][3])
        
        
        white_image = (tf.cast(self.I, tf.float32) - 100.) / 72.
        h = white_image
        for i, n in enumerate([10,20,30,40,50,60]):
            h = tf.contrib.layers.conv2d(h, 20, (3,3), stride=2, scope='conv%d'%(i))
        h = tf.contrib.layers.flatten(h)

        h2 = self.S
        h2 = tf.contrib.layers.fully_connected(h2, 30);
        h2 = tf.contrib.layers.fully_connected(h2, 60);
        h2 = tf.contrib.layers.fully_connected(h2, 90);

        h = tf.concat([h, h2], -1)
        
        predicted_state = tf.contrib.layers.fully_connected(h, len(VALID_ACTIONS) * len(STATE_VARS), activation_fn=None);
        predicted_state = tf.identity(predicted_state, name='predicted_state')
        self.predicted_state = tf.reshape(predicted_state, (-1, len(VALID_ACTIONS), len(STATE_VARS)))


        self.action = tf.placeholder(tf.int32, (None,), name='action') # action that was taken during game-play


        indices = tf.stack([tf.range(tf.size(self.action)), self.action], axis=1)
        self.action_conditioned_state = tf.gather_nd( self.predicted_state, indices, name='state_pred')
        self.label = tf.placeholder(tf.float32, (None,len(STATE_VARS)), name='label')
        self.action_loss = tf.reduce_sum(np.abs(LOSS_WEIGHT) * (self.label - self.action_conditioned_state)**2)
        self.loss = self.action_loss
        
        optimizer = tf.train.AdamOptimizer(0.001, 0.9, 0.999)
        self.train = optimizer.minimize(self.loss)

    
    def __call__(self, I, state, greedy_eps=1e-5, verbose=False):
        PA = sess.run(self.predicted_action, {self.I: I, self.S: [state]})[0]
        
        #action_score = np.dot(PS, SCORE_WEIGHT)
        action_score = np.dot(np.abs(PS), SCORE_WEIGHT)
        if verbose:
            print( PS )
            print( action_score )

        return VALID_ACTIONS[int(np.argmax(action_score))]
    
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

################################
###   Let's start training   ###
################################
EPOCHS = 100
SAMPLES_PER_LEVEL = 10
BS = 1
TRAIN_ITER_PER_EPOCH = 5
MAX_DATASET_SIZE = 10000

dataset = []
for epoch in range(EPOCHS):
    # Let's collect some data
    data = play_levels(P,greedy_eps=0.2)
    print( np.mean([s[-1] for i,s,a in data], axis=0) )
    for Is, Ss, As in data:
        samples = np.random.choice(len(Is)-1, size=SAMPLES_PER_LEVEL)
        for s in samples:
            #I = Is[max(0,s-3):s+1]
            #while len(I) < 4:
            #    I = np.concatenate( (I[0,None], I), axis=0 )
            I = Is[s]
            A = As[s]
            current_state = Ss[s]
            # Predict the delta in state
            #future_state = np.mean(Ss[s+1:s+11], axis=0)-Ss[s]
            current_position = int(abs(future_state[0])*1000)
            future_state = train_data[current_position][1:]

            dataset.append( (np.concatenate(I, axis=2), future_state, A, current_state) )
    
    # Trim the dataset and shuffle
    dataset = dataset[-MAX_DATASET_SIZE//2:]
    np.random.shuffle(dataset)
    
    # Train the network a bunch
    for it in range(TRAIN_ITER_PER_EPOCH):
        batch_data = [dataset[i] for i in np.random.choice(len(dataset), BS)]
        images = np.stack([I for I,F,A, C in batch_data], axis=0)
        future_state = np.stack([F for I,F,A, C in batch_data], axis=0)
        actions = np.stack([VALID_ACTIONS.index(A) for I,F,A, C in batch_data], axis=0)
        current_state = np.stack([C for I,F,A,C in batch_data], axis=0)
        loss, _ = sess.run( [P.loss, P.train], {P.I: images, P.action: actions, P.label: future_state, P.S: current_state} )
   print (loss)     
    
