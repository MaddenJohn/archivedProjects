import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from util import load
import numpy as np
import argparse
from sys import stdout
try:
	import graders
except:
	graders = None
	

class CheckFailed(Exception):
	def __init__(self, why):
		self.why = why
	
	def __str__(self):
		return "[E] Grading failed! %s"%self.why

class ContextManager:
	def __init__(self, on, off):
		self.on = on
		self.off = off
	
	def __enter__(self):
		self.on()
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.off()

class BaseGrader:
	def __init__(self, g, s):
		self.g, self.s = g, s
	
	def get_tensor(self, name):
		if not ':' in name: name = name + ':0'
		try:
			return self.g.get_tensor_by_name(name)
		except KeyError:
			return None
	
	def CHECK_TENSOR(self, name):
		if self.get_tensor(name) is None:
			raise CheckFailed("Make sure your compute graph provides a tensor named '%s'."%name)
	
	
	def CHECK_SHAPE(self, name, s):
		if isinstance(name, str):
			t = self.get_tensor(name)
		if t is None:
			raise CheckFailed("Make sure your compute graph provides a tensor named '%s' of shape %s."%(name, str(s)))
		S = t.get_shape().as_list()
		assert len(S) == len(s), "Shape mismatch for tensor '%s' expected %s got %s"%(t.get_name(), str(s), str(S))
		for a,b in zip(s,S):
			assert b is None or a == b, "Shape mismatch for tensor '%s' expected %s got %s"%(t, str(s), str(S))
	
	section = ""
	section_score = 0
	section_max = 0
	def BEGIN_SECTION(self, section):
		self.group = None
		self.section = section
		self.section_score = 0
		self.section_max = 0

	def END_SECTION(self):
		print( '\r * %-3s    [ %3d / %3d ]'%(self.section, self.section_score, self.section_max) )
		self.score += self.section_score
		self.section_score = 0
		self.section_max = 0
	
	def SECTION(self, section):
		def on(): self.BEGIN_SECTION(section)
		def off(): self.END_SECTION()
		return ContextManager(on, off)
	
	group = None
	group_ok = False
	def BEGIN_GROUP(self):
		self.group = 0
		self.group_ok = True
	
	def END_GROUP(self):
		if self.group is not None and not self.group_ok:
			self.section_score -= self.group
		self.group = None
	
	def GROUP(self):
		def on(): self.BEGIN_GROUP()
		def off(): self.END_GROUP()
		return ContextManager(on, off)
	
	def CASE(self, passed, score=1):
		from sys import stdout
		if passed:
			stdout.write('+')
			self.section_score += score
		else:
			stdout.write('-')
		self.section_max += score
		if self.group is not None:
			if not passed:
				self.group_ok = False
			else:
				self.group += 1
	
	BLACK_LIST = []
	WHITE_LIST = None
	ALLOWED_CONST = []
	def const_check(self, v):
		if self.ALLOWED_CONST is None: return True
		try:
			for a in v:
				if not self.const_check(a):
					return False
			return True
		except TypeError:
			return v in self.ALLOWED_CONST
	
	def op_check(self):
		for o in self.g.get_operations():
			if o.type == 'PyFunc':
				raise CheckFailed("Operation 'py_func' not allowed, in any assignment!")
			if False and o.type == 'Const' and o.type in self.BLACK_LIST:
				if o.name != 'UID' and o.name != 'AID':
					v = self.s.run(o.outputs[0])
					if not self.const_check(v):
						raise CheckFailed("Only constants allowed are %s got %s!"%(str(self.ALLOWED_CONST), str(v)))
			elif False and o.type in self.BLACK_LIST:
				raise CheckFailed("Operation '%s' not allowed in this assignment!"%o.type)
			
	def io_check(self):
		pass
	
	def __call__(self):
		try:
			self.op_check()
		except CheckFailed as e:
			print( str(e) )
			return 0
		
		try:
			self.io_check()
		except CheckFailed as e:
			print( str(e) )
			return 0
		except AssertionError as e:
			print( "[E] Grading failed! " + str(e) )
			return 0
		
		self.score = 0
		self.grade()
		return self.score


MAX_SUBMISSION_SIZE = 2**28

try:
    input_ = raw_input
except NameError:
    input_ = input
    
def yes_no(message, yes_list = ["yes", "y"], no_list = ["no", "n"], default=False):
    while True:
        choice = input_(message).lower()
        if not choice and default is not None:
            return default
        if choice in yes_list:
            return True
        if choice in no_list:
            return False
        print("Please respond with 'y' or 'n'")

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Grade an assignment')
	parser.add_argument('assignment')
	if graders is not None:
		parser.add_argument('grader')
	args = parser.parse_args()
	
	with tf.Session() as sess:
		print( 'Loading assignment ...' )
		try:
			graph = load(args.assignment)
		except IOError as e:
			print( e )
			exit(1)
		
		print( 'Finding grader ...' )
		if graders is not None:
			g = graders.find(args.grader)
			if g is None:
				print( '[E] No grader found, make sure the grader argument is set correctly' )
				exit(1)
		else:
			try:
				from _grader import Grader, TOTAL_SCORE
				def g(graph, sess):
					return Grader(graph, sess)()
				g.TOTAL_SCORE = TOTAL_SCORE
			except ImportError:
				print("grader.py not found, double check your starter code")
				exit(1)
		
		print( 'Grading locally ...' )
		score = g(graph, sess)
		print()
		print( 'total score locally                                        %3d / %3d'%(score, g.TOTAL_SCORE) )

