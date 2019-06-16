import numpy as np
import tensorflow as tf
from pykart import Kart
from time import sleep, time
from random import random
from pylab import *
import util

# Colors to visualize the labeling
COLORS = np.array([(0,0,0), (255,0,0), (0,255,0), (255,255,0), (0,0,255), (255,255,255)], dtype=np.uint8)
CROP_SIZE = 64
N_ACTION = 5
offsets = [0, 6, 15, 30, 60, 120]
# STEER_LEFT (1), STEER_RIGHT (2), ACCEL (4)
# BRAKE (8), NITRO (16), DRIFT (32), RESCUE (64), FIRE (128)

STATE_VARS = ['wrongway', 'finish_time', 'position_along_track', 'speed', 'distance_to_center', 'angle']
SCORE_WEIGHT = [-200, 1000000000000, 500, 0.001, -5, 0]
#VALID_ACTIONS = [5, 6, 20, 21, 22, 132, 133, 134] #8?
VALID_ACTIONS = [0,1,2,3,4, 5, 6]
K = Kart("lighthouse", 500, 500)
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

def getAction (state, okSave, A, idle_step):

    if ((state['wrongway'] or state['speed'] < 2) and okSave ):
        return 64, False

    return A, okSave

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
    As = []
    im, lbl = None, None
    best_progress, idle_step = 0, 0
    okSave = False
    total_Original = 0.0
    total_steps = 0.0
    while idle_step < max_idle_step and not state['finish_time']:
        A = policy(np.concatenate(([Is[0]]*3+Is)[-4:],axis=2), **kwargs)
        prevA = A
        print ("policyAction: ",A, idle_step, state['position_along_track'])
        As.append(A)
        A, okSave = getAction(state, okSave, A, idle_step)
        if (A == 64 and prevA == 4):
            idle_step = 0
        try:
            state, obs = K.step(int(A))
        except TypeError:
            print ("TypeError")
            break
        Is.append(obs)
        Ss.append([state[s] for s in STATE_VARS])
        Ss[-1][-1] = abs(Ss[-1][-1])
        if (state['speed'] > 2):
            okSave = True
        idle_step += 1
        if best_progress < state['position_along_track'] and state['speed'] > 0.1:
            best_progress = state['position_along_track']
            idle_step = 0

        pause(0.01)
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
    #print (STATE_VARS)
    #print (SCORE_WEIGHT)
    #print (np.mean(score, axis=0))
    return np.mean(score, axis=0)

# Let's now train our own neural policy
sess = tf.Session()

class CNNPolicy:
    # Only ever create one single CNNPolicy network per graph, otherwise things will FAIL!
    def __init__(self):
        train_data = load_dataset('0cp_hc')
        data = []
        for x in range(150):
            data.append(x)

        for k in train_data:
            if (k < 0.15):
                #print (k, train_data[k])
                index = abs(int(k*1000))
                #print (index)
                data[index] = (k, train_data[k])
        #print (data)
        for s in data:
            print (s)
        valid_data = load_dataset('1cp')
        self.S = tf.placeholder(tf.float32, (None, len(STATE_VARS)), name='state')
        current_position, current_angle, current_distance_to_center, current_action = round(state['position_along_track'], 3), state['angle'], state['distance_to_center'],  A
        
        #current_position, current_angle, current_distance_to_center, current_action = round(state['position_along_track'], 3), state['angle'], state['distance_to_center'],  A
        valid_action, valid_position_along_track, valid_distance_to_center, valid_angle = float(train_data[current_position][0]), float(train_data[current_position][1]), float(train_data[current_position][2]), float(train_data[current_position][3])
        print (current_position, current_angle, current_distance_to_center, current_action)
        print (valid_action, valid_position_along_track, valid_distance_to_center, valid_angle)
        temp = int(valid_action)

        current_action = tf.identity(tf.cast(current_action, tf.float32), name='current_action')
        current_position = tf.identity(current_position, name='current_position')
        current_angle = tf.identity(current_angle, name='current_angle')
        current_distance_to_center = tf.identity(current_distance_to_center, name='current_distance_to_center')

        valid_action = tf.identity(valid_action, name='valid_action')
        valid_position_along_track = tf.identity(valid_position_along_track, name='valid_position_along_track')
        valid_distance_to_center = tf.identity(valid_distance_to_center, name='valid_distance_to_center')
        valid_angle = tf.identity(valid_angle, name='valid_angle')



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
        print (h)
        action_logit = tf.contrib.layers.fully_connected(h, len(VALID_ACTIONS), activation_fn=None)

        # Use a cross entropy for the action and is_dying, L2 for position and coin.
        #print ("VA", valid_action)
        #valid_reshape_action = valid_action
        #rs = tf.convert_to_tensor(valid_action)
        #print(rs)
        #rs = tf.reshape(valid_action, (6, len(VALID_ACTIONS)))
        #print (rs)
        print ("-------***TEMP:", temp)
        onehot_valid_action = tf.one_hot( indices = temp, depth = len(VALID_ACTIONS)  )
        print (onehot_valid_action)
       # print (onehot_valid_action)
        print (action_logit)

        self.action = tf.placeholder(tf.int32, (None,), name='action')
        #valid_reshape_action = tf.reshape(tf.cast(valid_action, tf.float32), (6, len(VALID_ACTIONS)))
        #action_loss = tf.reduce_mean( tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.cast(onehot_valid_action, tf.float32), logits=action_logit) )
        action_loss = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(labels=tf.cast(onehot_valid_action, tf.float32), logits=action_logit) )
        #action_loss = tf.reduce_mean( tf.nn.l2_loss(valid_action-current_action) )
        #is_dying_loss = tf.reduce_mean( tf.nn.sigmoid_cross_entropy_with_logits(labels=tf.cast(future_is_dying, tf.float32), logits=future_is_dying_logit) )
        center_loss = tf.reduce_mean( tf.nn.l2_loss(valid_distance_to_center-current_distance_to_center) )
        position_loss = tf.reduce_mean( tf.nn.l2_loss(valid_position_along_track-current_position) )
        angle_loss = tf.reduce_mean( tf.nn.l2_loss(valid_angle-current_angle) )
        #self.loss = center_loss + position_loss + angle_loss + 500000 * action_loss
        self.loss = action_loss
        #print("Loss:", self.loss, "C", center_loss, "P", position_loss, "An", angle_loss, "Ac", action_loss)

        #pred_is_dying = tf.identity(future_is_dying_logit > 0.5, name='predicted_is_dying')
        #pred_position = tf.identity(future_position_logit, name='predicted_position')
        #pred_coins = tf.identity(future_coins_logit, name='predicted_coins')

        # Let's weight the regularization loss down, otherwise it will hurt the model performance
        # You can tune this weight if you wish
        regularization_loss = tf.losses.get_regularization_loss()
        total_loss = self.loss + 1e-6 * regularization_loss

        # Adam will likely converge much faster than SGD for this assignment.
        optimizer = tf.train.AdamOptimizer(0.001, 0.9, 0.999)

        # use that optimizer on your loss function (control_dependencies makes sure any 
        # batch_norm parameters are properly updated)
        with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
            opt = optimizer.minimize(total_loss)
            self.train = opt

        
        self.label = tf.placeholder(tf.float32, (None,len(STATE_VARS)), name='label')
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
        #print ("a1")
        samples = np.random.choice(len(Is)-1, size=SAMPLES_PER_LEVEL)
        for s in samples:
            I = Is[max(0,s-3):s+1]
            while len(I) < 4:
                I = np.concatenate( (I[0,None], I), axis=0 )
            A = As[s]
            current_state = Ss[s]
            # Predict the delta in state
            future_state = np.mean(Ss[s+1:s+11], axis=0)-Ss[s]
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
        #print ("a2")
        current_state = np.stack([C for I,F,A,C in batch_data], axis=0)
        loss, _ = sess.run( [P.loss, P.train], {P.I: images, P.action: actions, P.label: future_state, P.S: current_state} )
        #print ("a3")
    print ("L", loss) 
    
print( score_policy(P) )

###########################################
###   Visualize how well tux is doing   ###
###########################################
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

util.save('imitation.tfg', session=sess)
