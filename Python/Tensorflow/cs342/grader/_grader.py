from grade import BaseGrader
CHECKSUM='a2_public'
TOTAL_SCORE=50

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	def io_check(self):
		# Make sure input accepts a list of random numbers
		self.CHECK_SHAPE('input', [None, 2])
		self.CHECK_SHAPE('linear_output', [None, 1])
		self.CHECK_SHAPE('nonlinear_output', [None, 1])

	def grade(self):
		import numpy as np
		np.random.seed(0)
		input = self.get_tensor('input')
		linear_output = self.get_tensor('linear_output')
		nonlinear_output = self.get_tensor('nonlinear_output')

		with self.SECTION("linear classification accuracy     "):
			for it in range(5):
				inputs = np.random.rand(10000, 2)
				labels = (np.sum(inputs * inputs, axis=1) < 1.0).astype('float')
				linear_out = np.squeeze(self.s.run(linear_output, {input: inputs}))
				linear_out = (linear_out > 0.0).astype('float')
				eq = (labels == linear_out).astype('float')
				accuracy = np.mean(eq)
				#print('Linear classifier accuracy: ' + str(accuracy))
				#print('Accuracy must be above 0.90')
				self.CASE(accuracy > 0.90, score=5)
		
		with self.SECTION("nonlinear classification accuracy  "):
			for it in range(5):
				inputs = np.random.rand(10000, 2)
				labels = (np.sum(inputs * inputs, axis=1) < 1.0).astype('float')
				nonlinear_out = np.squeeze(self.s.run(nonlinear_output, {input: inputs}))
				nonlinear_out = (nonlinear_out > 0.0).astype('float')
				eq = (labels == nonlinear_out).astype('float')
				accuracy = np.mean(eq)
				#print('Nonlinear classifier accuracy: ' + str(accuracy))
				#print('Accuracy must be above 0.95')
				self.CASE(accuracy > 0.95, score=5)
		
