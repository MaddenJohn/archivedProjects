from grade import BaseGrader
import tensorflow as tf
import numpy as np
CHECKSUM='a2_public'
TOTAL_SCORE=80

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	def io_check(self):
		# Make sure input accepts a list of random numbers
		self.CHECK_SHAPE('input', [None, 64, 64, 3])
		self.CHECK_SHAPE('sr/output', [None, 1])
		self.CHECK_SHAPE('ohr/output', [None, 6])
		self.CHECK_SHAPE('ll/output', [None, 6])
		self.CHECK_SHAPE('l2/output', [None, 6])

	def grade(self):
		np.random.seed(0)
		inputs = self.get_tensor('input')
		labels = self.get_tensor('labels')
		sr_output = self.get_tensor('sr/output')
		ohr_output = self.get_tensor('ohr/output')
		ll_output = self.get_tensor('ll/output')
		l2_output = self.get_tensor('l2/output')

		W, H, Ch = 64, 64, 3
		data = np.fromfile('tux_val.dat', dtype=np.uint8).reshape((-1, W*H*3+1))
		val_images, val_labels = data[:, :-1].reshape((-1,H,W,3)), data[:, -1]
		
		outputs = {'sr': sr_output, 'ohr': ohr_output, 'll': ll_output, 'l2': l2_output}
		accuracies = {'sr': 0.2, 'ohr': 0.85, 'll': 0.90, 'l2': 0.85}
		names = {'sr': 'Scalar Regression', 'ohr': 'One-hot Regression', 'll': 'Softmax+Log-Likelihood', 'l2': 'Softmax+L2-Regression'}

		# Check accuracies
		for o in outputs:
			acc = accuracies[o] / 2.0
			acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(outputs[o], 1), labels), tf.float32))
			accuracy = self.s.run(acc_op, {inputs: val_images, labels: val_labels})
			print(names[o] + ' validation accuracy: ' + str(accuracy))
			for it in range(5):
				with self.SECTION(names[o] + ' validation accuracy > ' + str(acc) + '\t\t\t'):
					self.CASE(accuracy > acc, score=4)
					acc += accuracies[o] / 8.0
			print('')
