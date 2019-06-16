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
		self.CHECK_SHAPE('input', [None, 64, 64, 3])
		self.CHECK_SHAPE('output', [None, 6])

	def grade(self):
		np.random.seed(0)
		inputs = self.get_tensor('input')
		labels = self.get_tensor('labels')
		outputs = self.get_tensor('output')

		W, H, Ch = 64, 64, 3
		data = np.fromfile('tux_val.dat', dtype=np.uint8).reshape((-1, W*H*3+1))
		val_images, val_labels = data[:, :-1].reshape((-1,H,W,3)), data[:, -1]
		
		### 50 ###
		# Check accuracy - need above 90% for full credit
		#with self.SECTION('Classification validation accuracy\t\t\t\t'):
		acc_op = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(outputs, 1), labels), tf.float32))
		accuracy = self.s.run(acc_op, {inputs: val_images, labels: val_labels})
		print('Validation Accuracy: ' + str(accuracy))
		acc_thresholds = [0.70, 0.75, 0.80, 0.85, 0.90]
		for it in range(5):
			with self.SECTION('accuracy > ' + str(acc_thresholds[it])):
				self.CASE(accuracy > acc_thresholds[it], score=10)

		### 10 ###
		# Check number of conv layers
		with self.SECTION('There must be 5 convolutional layers\t\t\t\t'):
			convs = [o.name for o in self.g.get_operations() if o.name.startswith('conv')]
			self.CASE(all([c.split('/')[0] in ['conv1', 'conv2', 'conv3', 'conv4', 'conv5'] for c in convs]), score=10)

		### 10 ###
		# Check for pooling layer
		with self.SECTION('There must be 1 pooling layer\t\t\t\t'):
			self.CASE(len([o.name for o in self.g.get_operations() if o.name.startswith('pool')]) == 1, score=10)

		### 10 ###
		# Check use of softmax + log-likelihood
		with self.SECTION('Use of softmax + log-likelihood\t\t\t\t'):
			self.CASE(any([o.name.startswith('SparseSoftmaxCrossEntropyWithLogits') for o in outputs.consumers()]), score=10)

		### 10 ###
		# Check each layer has stride size of 2
		with self.SECTION('Each layer must have a stride size of 2\t\t\t\t'):
			self.CASE([self.g.get_operation_by_name('conv' + str(i) + '/convolution').get_attr('strides')[1:3] == [2.0, 2.0] for i in range(1, 6)], score=10)

		### 10 ###
		# Check number of parameters
		with self.SECTION('Number of parameters\t\t\t\t'):
			self.CASE(np.sum([v.get_shape().num_elements() for v in tf.trainable_variables()]) < 100000, score=10)
		
