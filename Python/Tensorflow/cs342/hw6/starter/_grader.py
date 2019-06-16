from grade import BaseGrader
import tensorflow as tf
import numpy as np
CHECKSUM='a2_public'
TOTAL_SCORE=50

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	def io_check(self):
		# Make sure input accepts a list of random numbers
		self.CHECK_SHAPE('inputs', [None, 64, 64, 3])
		self.CHECK_SHAPE('output', [None, 6])

	def grade(self):
		np.random.seed(0)
		inputs = self.get_tensor('inputs')
		labels = self.get_tensor('labels')
		outputs = self.get_tensor('output')

		W, H, Ch = 64, 64, 3
		data = np.fromfile('tux_val.dat', dtype=np.uint8).reshape((-1, W*H*3+1))
		val_images, val_labels = data[:, :-1].reshape((-1,H,W,3)), data[:, -1]
		
		acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(outputs, 1), labels), tf.float32))
		accuracy = self.s.run(acc_op, {inputs: val_images, labels: val_labels})
		print('Validation Accuracy: ' + str(accuracy))
		acc_thresholds = [0.93, 0.94]
		acc_scores = [25, 25]
		for it in range(len(acc_thresholds)):
			with self.SECTION('accuracy > ' + str(acc_thresholds[it])):
				self.CASE(accuracy > acc_thresholds[it], score=acc_scores[it])
