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
		total_lbl, total_cor = np.zeros(6)+1e-10, np.zeros(6)
		I0 = tf.placeholder(tf.float32, shape=(1, None, None, 3))
		LR = tf.layers.average_pooling2d(I0, 5, 4, padding='SAME', name='image_lr')

		losses = []
		for it in tf.python_io.tf_record_iterator('valid.tfrecord'):
		    example = tf.train.Example()
		    example.ParseFromString(it)
		    I = np.frombuffer(example.features.feature['image_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256, 3)
		    L = np.frombuffer(example.features.feature['label_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256)
		    
		    lr_val = self.s.run(LR, {I0: I[None]})
		    r = self.s.run('output:0', {'image_lr:0':lr_val, 'label:0': L[None]})[0]
		    losses.append(np.mean(np.abs(r.astype(np.float32)-I)))
		mean_diff = np.mean(losses)
		print( 'Mean absolute difference', mean_diff )
		with self.SECTION('Class Accuracy'):
			self.CASE(True, score=min(abs(min((mean_diff-14.0),0.0)), 5.0)*20.0)
		with self.SECTION('Extra Credit'):
			self.CASE(mean_diff <= 8.0, score=5)
			self.CASE(mean_diff <= 7.0, score=5)
			self.CASE(mean_diff <= 6.0, score=5)
			self.CASE(mean_diff <= 5.0, score=5)
			