def save(output_file, graph=None, session=None):
	import tensorflow as tf
	from glob import glob
	from zipfile import ZipFile
	from os import path, remove, rmdir
	from tempfile import mkdtemp
	
	if graph is None:
		graph = tf.get_default_graph()
	if session is None:
		session = tf.get_default_session()
	if session is None:
		session = tf.Session()
	
	if '.meta' in output_file:
		print( '[W] Putting ".meta" in our filename is asking for trouble!')
		return None
	
	tmp_dir = mkdtemp()
	tmp_output = path.join(tmp_dir, path.basename(output_file))
	with graph.as_default():
		saver = tf.train.Saver(allow_empty=True)
		saver.save(session, tmp_output, write_state=False)
	
	of = ZipFile(output_file, 'w')
	for f in glob(tmp_output+'.*'):
		of.write(f, path.basename(f))
		remove(f)
	of.close()
	rmdir(tmp_dir)

def load(input_file, graph=None, session=None):
	import tensorflow as tf
	from glob import glob
	from os import path
	from shutil import rmtree
	from tempfile import mkdtemp
	from zipfile import ZipFile
	
	tmp_dir = mkdtemp()
	
	f = ZipFile(input_file, 'r')
	f.extractall(tmp_dir)
	f.close()
	
	# Find the model name
	meta_files = glob(path.join(tmp_dir, '*.meta'))
	if len(meta_files) < 1:
		raise IOError( "[E] No meta file found, giving up" )
	if len(meta_files) > 1:
		raise IOError( "[E] More than one meta file found, giving up" )
	
	meta_file = meta_files[0]
	model_file = meta_file.replace('.meta', '')
	
	if graph is None:
		graph = tf.get_default_graph()
	if session is None:
		session = tf.get_default_session()
	if session is None:
		session = tf.Session()
	
	# Load the model in TF
	with graph.as_default():
		saver = tf.train.import_meta_graph(meta_file)
		if saver is not None:
			saver.restore(sessioin, model_file)
	rmtree(tmp_dir)
	return graph

	
