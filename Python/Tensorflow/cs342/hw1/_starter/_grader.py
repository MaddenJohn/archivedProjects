from grade import BaseGrader
CHECKSUM='a1_public'
TOTAL_SCORE=50

class Grader(BaseGrader):
	def __init__(self, g, s):
		BaseGrader.__init__(self, g, s)
	
	BLACK_LIST = ['Const', 'Acos', 'Asin', 'Atan']
	ALLOWED_CONST = [0, 1, 1.0, 2]
	
	def io_check(self):
		# Make sure input accepts a list of random numbers
		self.CHECK_SHAPE('input', [None, 2])
		self.CHECK_SHAPE('output', [])
	
	def grade(self):
		import numpy as np
		np.random.seed(0)
		input = self.get_tensor('input')
		output = self.get_tensor('output')
		with self.SECTION("Testing stochasticity"):
			for it in range(5):
				with self.GROUP():
					for g in range(5):
						r = np.std([float(self.s.run(output, {input: np.random.random((1,2))})) for it in range(100)])
						self.CASE( r > 5e-2 )

		with self.SECTION("Approximating pi with 75 samples"):
			for it in range(5):
				with self.GROUP():
					for g in range(5):
						r = float(self.s.run(output, {input: np.random.random((5,2))}))
						self.CASE( np.abs(r - np.pi / 4) < 0.05 )
