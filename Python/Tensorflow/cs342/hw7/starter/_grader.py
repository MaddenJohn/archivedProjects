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
		self.CHECK_SHAPE('inputs', [None, 64, 64, 3])
		self.CHECK_SHAPE('output', [None, None, None])

	def grade(self):
		total_lbl, total_cor = np.zeros(6)+1e-10, np.zeros(6)
		for it in tf.python_io.tf_record_iterator('valid.tfrecord'):
		    example = tf.train.Example()
		    example.ParseFromString(it)
		    I = np.frombuffer(example.features.feature['image_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256, 3)
		    L = np.frombuffer(example.features.feature['label_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256)
		    
		    P = self.s.run('output:0', {'inputs:0':I[None]})
		    total_lbl += np.bincount(L.flat, minlength=6)
		    total_cor += np.bincount(L.flat, (P==L).flat, minlength=6)
		mca = np.mean(total_cor / total_lbl) * 100
		print (mca)
		with self.SECTION('Class Accuracy'):
			self.CASE(True, score=(max(min((mca-33.0)/33.0,1.0),0.0)*100.0))
		with self.SECTION('Extra Credit'):
			self.CASE(mca > 70, score=5)
			self.CASE(mca > 75, score=5)
			self.CASE(mca > 80, score=5)