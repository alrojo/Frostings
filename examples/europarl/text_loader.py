from frostings.loader import *


def remove_samples(samples):
	# remove input sentences that are too short or too long
	samples = [(x, t) for x, t in samples if len(x) > 1 and len(x) <= 400]

	# remove target sentences that are too short or too long
	samples = [(x, t) for x, t in samples if len(t) > 1 and len(t) <= 450]

	return samples

# prepare a dictionary for mapping characters to integer tokens

def get_dictionary_char(langs = ['en', 'fr']):
	alphabet = dict()
	for lang in langs:
		with open('./data/alphabet.'+lang, 'r') as f:
			alphabet[lang] = f.read().split('\n')
	alphadict = []
	for lang in langs:
		alphadict.append({character: idx for idx, character in enumerate(alphabet[lang])})
	return alphadict

def char_encoding(in_string):

	pass

def word_encoding(in_string):
	pass

def spaces(in_string):
	pass

def char_length(in_string):
	return len(in_string)

def word_length(in_string):
	pass

class TextLoadMethod(LoadMethod):

	def _load_data(self):
		with open("data/train/europarl-v7.fr-en.en", "r") as f:
			self.train_X = f.read().split("\n")
		with open("data/train/europarl-v7.fr-en.fr", "r") as f:
			self.train_t = f.read().split("\n")
		self.samples = zip(self.train_X, self.train_t)

	def _preprocess_data(self):
		if self.samples == None:
			self._load_data()
		self.samples = sorted(self.samples, key=lambda (X, t): len(X)*10000 + len(t))
		# remove samples not of interest
		self.samples = remove_samples(self.samples)
		for sample_idx, sample in enumerate(self.samples):
			my_s = []
			for elem in sample:# samples should be tuple(train_X, train_t)
				# char encoding
				my_s.append(char_encoding(elem))
				# word encoding
				my_s.append(word_encoding(elem))
				# spaces
				my_s.append(spaces(elem))
				# char length
				my_s.append(char_length(elem))
				# word length
				my_s.append(word_length(elem))
			self.samples[sample_idx] = tuple(my_s) + sample # concats with original sample

def get_max_length(encodings):
	pass

class TextBatchGenerator(BatchGenerator):

	def _make_batch_holder(self, max_length):
		self.batch = []
		pass # should make a "holder", e.g. self.batch.append(np.zeros((self.batch_info.batch_size, max_length, encoding_size) and .append a np.zeros for sequences_lengths, spaces etc.

	def _make_batch(self):
		self._make_batch_holder()
		for _ in range(len(self.samples)):
			pass # Should fit each sample to the holder
		return self.batch

# Chunk loader is not thought of here, but it should fit without modifying it

### RUNNING THE TEXT LOADER ###

text_load_method = TextLoadMethod()
text_load_method(10000) # remember that it has a __call__ function

sample_info = SampleInfo(len(text_load_method.samples)) # needs to know how many samples we have, so it can make an idx for all of them.
sample_gen = SampleGenerator(text_load_method, sample_info) # generates one sample which consists of several elements sample = (elem, elem, elem)
batch_info = BatchInfo(batch_size=32)
text_batch_gen = TextBatchGenerator(sample_gen, batch_info) # Generates a batch, being a tuples
chunk_info = ChunkInfo()
chunk_gen = ChunkGenerator(text_batch_gen, chunk_info)
# should be used like.
# for train_X_char_enc, train_X_word_enc, train_X_sequence_length ... in text_batch_gen.gen_batch():
