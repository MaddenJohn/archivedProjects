from grade import BaseGrader
import tensorflow as tf
import numpy as np
CHECKSUM='a2_public'
TOTAL_SCORE=100

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	def io_check(self):
		# Make sure input accepts a list of random numbers
		try:
			self.g.get_tensor_by_name('input')
			self.CHECK_SHAPE('input', [None, 64, 64, 3])
		except:
			self.CHECK_SHAPE('Placeholder', [None, 64, 64, 3])
		self.CHECK_SHAPE('output', [None, 6])

	def grade(self):
		np.random.seed(0)
		inputs = self.get_tensor('input')
		if inputs is None:
			inputs = self.get_tensor('Placeholder')
		labels = self.get_tensor('labels')
		outputs = self.get_tensor('output')

		W, H, Ch = 64, 64, 3
		data = np.fromfile('tux_val.dat', dtype=np.uint8).reshape((-1, W*H*3+1))
		val_images, val_labels = data[:, :-1].reshape((-1,H,W,3)), data[:, -1]
		
		acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(outputs, 1), labels), tf.float32))
		accuracy = self.s.run(acc_op, {inputs: val_images, labels: val_labels})
		print('Validation Accuracy: ' + str(accuracy))
		acc_thresholds = [0.93, 0.94, 0.95, 0.96, 0.97, 0.98]
		acc_scores = [33, 33, 34, 10, 10, 10]
		for it in range(6):
			with self.SECTION('accuracy > ' + str(acc_thresholds[it])):
				self.CASE(accuracy > acc_thresholds[it], score=acc_scores[it])
