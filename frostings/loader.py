import numpy as np
import os
import utils

from . import utils

# Method YOU should implement!
class LoadMethod(object):

	def __init__(self):
		self._prepare_data()

	def _load_data(self):
		self.train_X = []
		self.train_t = []
		self.samples = zip(self.train_X, self.train_t)

	def _preprocess_data(self):
		pass

	def _prepare_data(self):
		if not os.path.exists("data/train.npy.gz"):
			self._load_data()
			self._preprocess_data()
		else:
			self.samples = utils.load_gz("data/train.npy.gz")

	def __call__(self, idx):
		return self.samples[idx]

class SampleInfo(object):

	def __init__(self, samples_length, samples_idx=None):
		self.samples_length = samples_length
		self.samples_idx = samples_idx
		print("SampleInfo initated")

class SampleGenerator(object):

	def __init__(self, load_method, sample_info, shuffle=False, repeat=False):
		self.load_method = load_method
		self.sample_info = sample_info
		self.shuffle = shuffle
		self.repeat = repeat
		print("ElemGenerator initiated")

	def _shuffle_paths(self, state):
		np.random.set_state(state)
		np.random.shuffle(self.samples_idx)

	def gen_sample(self):
		while True:
			if self.shuffle:
				state = np.random.get_state()
				self._shuffle_paths(state)
			for num in xrange(self.sample_info.samples_length):
				yield self.load_method(num)
			if not self.repeat:
				break

class BatchInfo(object):

	def __init__(self, batch_size):
		self.batch_size = batch_size
		print("BatchInfo initiated")

class BatchGenerator(object):

	def __init__(self, sample_generator, batch_info):
		self.sample_generator = sample_generator
		self.batch_info = batch_info
		self.samples = []

	def _make_batch_holder(self):
		pass # undecided on the general purpose structure ... See examples for implementation

	def _make_batch(self):
		pass # undecided on the general purpose structure ... See examples for implementation

	def gen_batch(self):
		self.sample_idx = 0
		for sample in self.sample_generator.gen_sample():
			self.samples.append(sample)
			self.sample_idx += 1
			if self.sample_idx >= self.batch_info.batch_size:
				yield self._make_batch()
		if self.sample_idx > 0:
			yield self._make_batch()

class ChunkInfo(object):

	def __init__(self, chunk_size=4096, num_chunks=800):
		self.chunk_size = chunk_size
		self.num_chunks = num_chunks
		print("ChunkInfo initiated")

class ChunkGenerator(object):

	def __init__(self, batch_generator, chunk_info, rng=np.random):
		self.batch_generator = batch_generator
		self.chunk_info = chunk_info
		self.rng = rng
		self.batches = []
		print("ChunkGenerator initiated")

	def _make_chunk_holder(self):
		self.chunk = [] # not in __init__ to reset it at every call
		self.chunk.append([]) # where the batch is located
		self.chunk.append(self.batch_idx) # pasting the idx
		self.batch_idx = 0

	def _make_chunk(self):
		self._make_chunk_holder()
		for _ in range(len(self.batches)): # smarter solution?
			self.chunk[0].append(self.batches.pop())
		return self.chunk

	def gen_chunk(self):
		self.batch_idx = 0
		for batch in self.batch_generator.gen_batch():
			self.batches.append(batch)
			self.batch_idx += 1
			if self.batch_idx >= self.chunk_info.chunk_size:
				yield self._make_chunk()
		if self.batch_idx > 0:
			yield self._make_chunk()
