from grade import BaseGrader
import tensorflow as tf
import numpy as np
CHECKSUM='a2_public'
TOTAL_SCORE=100

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	def io_check(self):
		pass

	def grade(self):
		N_ACTION = 5 
		offsets = [0, 6, 15, 30, 60, 120]

		action_p = tf.placeholder(tf.int32, shape=(None))
		dying_p = tf.placeholder(tf.bool, shape=(None))
		pos_p = tf.placeholder(tf.float32, shape=(None))
		coins_p = tf.placeholder(tf.float32, shape=(None))

		pred_action = self.get_tensor('predicted_action')
		future_position_logit = self.get_tensor('predicted_position')
		pred_is_dying = self.get_tensor('predicted_is_dying')
		future_coins_logit = self.get_tensor('predicted_coins')
		#####################
		action_accs = []
		dying_accs = []
		pos_losses = []
		coin_losses = []
		index = 0
		temp = 0
		#Count: 2194 
		for it in tf.python_io.tf_record_iterator('future_val.tfrecord'):
			temp += 1
		print("Count: " + str(temp))
		for it in tf.python_io.tf_record_iterator('future_val.tfrecord'):
		    index += 1
		    if index % 10 == 0:
		        print(index)
		    example = tf.train.Example()
		    example.ParseFromString(it)
		    
		    # Get ground truth inputs
		    I = np.expand_dims(np.frombuffer(example.features.feature['image_raw'].bytes_list.value[0], dtype=np.uint8).reshape(64, 64, 9), axis=0)
		    A = example.features.feature['action'].int64_list.value[0]
		    action = tf.stack([tf.bitwise.bitwise_and(action_p, (1<<i)) > 0 for i in range(N_ACTION)])
		    current_position = [example.features.feature['position_0'].float_list.value[0]]
		    current_is_dying = [example.features.feature['is_dying_0'].int64_list.value[0]]
		    current_coins = [example.features.feature['coins_0'].int64_list.value[0]]
		    
		    # Get ground truth labels
		    val_future_pos = np.expand_dims(np.array([example.features.feature['position_%d'%o].float_list.value[0] for o in range(1,len(offsets))]), axis=-1)
		    val_future_dying = np.expand_dims(np.array([example.features.feature['is_dying_%d'%o].int64_list.value[0] for o in range(1,len(offsets))]), axis=-1)
		    val_future_coins = np.expand_dims(np.array([example.features.feature['coins_%d'%o].int64_list.value[0] for o in range(1,len(offsets))]), axis=-1)
		    
		    future_position = tf.stack(tf.cast(pos_p, tf.float32))
		    future_is_dying = tf.stack(tf.cast(dying_p, tf.float32))
		    future_coins = tf.stack(tf.cast(coins_p, tf.float32))
		    
		    action, future_position, future_is_dying, future_coins = self.s.run([action, future_position, future_is_dying, future_coins], {action_p: A, pos_p: val_future_pos, dying_p: val_future_dying, coins_p: val_future_coins})
		    action = np.expand_dims(np.array(action), axis=0)
		    
		    # Make predictions
		    action_pred, pos_pred, dying_pred, coins_pred = self.s.run([tf.cast(pred_action, tf.float32), future_position_logit, tf.cast(pred_is_dying, tf.float32), future_coins_logit], {'images:0': I, 'action:0': action, 'current_position:0': current_position, 'current_is_dying:0': current_is_dying, 'current_coins:0': current_coins})
		    action_pred = action_pred[0]
		    pos_pred = pos_pred[0]
		    dying_pred = dying_pred[0]
		    coins_pred = coins_pred[0]
		    
		    # Score predictions
		    val_action_acc = np.mean((action_pred == action).astype('float32'))
		    val_dying_acc = np.mean((dying_pred == future_is_dying).astype('float32'))
		    val_pos_acc = np.mean((pos_pred - future_position) ** 2)
		    val_coin_acc = np.mean((coins_pred - future_coins) ** 2)
		    
		    action_accs.append(val_action_acc)
		    dying_accs.append(val_dying_acc)
		    pos_losses.append(val_pos_acc)
		    coin_losses.append(val_coin_acc)
		    
		action_acc = np.mean(action_accs)
		dying_acc = np.mean(dying_accs)
		pos_loss = np.mean(pos_losses)
		coin_loss = np.mean(coin_losses)
		print('Action accuracy: ' + str(action_acc))
		print('Is-Dying accuracy: ' + str(dying_acc))
		print('Position L2: ' + str(pos_loss))
		print('Coin L2: ' + str(coin_loss))

		with self.SECTION('Action Accuracy'): # 80% accuracy = 0pts --> 85% accuracy = 25pts
			self.CASE(True, score=max(min((action_acc-0.8),0.0),0.05)*500.0)
		with self.SECTION('Death Accuracy'): # 90% accuracy = 0pts --> 99% accuracy = 25pts
			self.CASE(True, score=max(min((dying_acc-0.9),0.0),0.09)*278.0)
		with self.SECTION('Postion Accuracy'): # L2=0.1 = 0pts --> L2=0.01 = 25pts
			self.CASE(True, score=(min(abs(min((pos_loss-0.1),0.0)), 0.09)/0.09)*25.0)
		with self.SECTION('Coin Accuracy'): # L2=0.1 = 0pts --> L2=0.001 = 25pts
			self.CASE(True, score=(min(abs(min((coin_loss-0.1),0.0)), 0.099)/0.099)*25.0)
