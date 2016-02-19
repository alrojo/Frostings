import numpy as np

class LoadMethod(object):
	def __init__():
		pass
	def __call__():
		pass

class ElemGenerator(object):
	def __init__(self, LoadMethod, paths=[], labels=None, shuffle=False, repeat=False):
		self.LoadMethod = LoadMethod
		self.samples_length = len(self.LoadMethod.samples)
		self.samples_idx = range(self.sample_length)
		self.shuffle = shuffle
		self.repeat = repeat
		print("ElemGenerator initiated")

	def _shuffle_paths(self, state):
		print("_shuffle_paths started")
		np.random.set_state(state)
		np.random.shuffle(self.samples_idx)
		print("paths have been shuffled")

	def _load_elem(self, num):
		print("_load_elem started")
		path = self.paths[num]
		print("path is")
		print(path)
		return self.LoadMethod(num)

	def gen_elem(self):
		print("gen_elem started")
		while True:
			if self.shuffle:
				state = np.random.get_state()
				self._shuffle_paths(state)
			print("sh*ts going down")
			for num in xrange(self.samples_length):
				yield self._load_elem(num)
			if not self.repeat:
				break

class ElemInfo(object):
	def __init__(self, labels=False, elem_shape=None, label_shape=None, elem_dtype=None, label_dtype=None):
		self.elem_shape = elem_shape
		self.label_shape = label_shape
		self.elem_dtype = elem_dtype
		self.label_dtype = label_dtype

class ChunkInfo(object):
	def __init__(self, chunk_size=4096, num_chunks=800):
		self.chunk_size = chunk_size
		self.num_chunks = num_chunks

class ChunkGenerator(object):
	def __init__(self, ElemGenerator, ElemInfo=None, ChunkInfo=None, rng=np.random):
		self.ElemGenerator = ElemGenerator
		self.ElemInfo = ElemInfo
		self.ChunkInfo = ChunkInfo
		self.rng = rng
		self.chunk = []
		print("ChunkGenerator initiated")

	def _make_chunk(self):
		chunk_elem = np.empty(self.ChunkInfo.chunk_size, dtype='object')
		self.chunk.append(chunk_elem)
		if self.ElemGenerator.labels is not None:
			chunk_label = np.empty(self.ChunkInfo.chunk_size, dtype='object')
			self.chunk.append(chunk_label)

	def _add_chunk(self, sample, idx):
		for s, c in zip(sample, self.chunk):
			c[idx] = s

	def gen_chunk(self):
		print("get_chunk started")
		self._make_chunk()
		idx = 0
		for sample in self.ElemGenerator.gen_elem():
			print("uhh, sample!")
			print(type(sample))
			self._add_chunk(sample, idx)
			idx += 1
			if idx >= self.ChunkInfo.chunk_size:
				yield self.chunk, idx
				_make_chunk() # Cleaning purposes
				idx = 0
		if idx > 0:
			yield self.chunk, idx



