import skimage.io
import glob
import numpy as np

from frostings import loader
# set-up
# TODO - make it work for mnist (data folder is not mnist)

load_method = skimage.io.imread
paths = glob.glob("./data/*")
elem_gen = loader.ElemGenerator(load_method, paths)

elem_info = loader.ElemInfo()
chunk_info = loader.ChunkInfo()

chunk_generator = loader.ChunkGenerator(elem_gen, elem_info, chunk_info)

for chunk, idx in chunk_generator.gen_chunk():
	print("--- JOHN ---")
	print(idx)
	print("chunk list")
	print(type(chunk))
	print(len(chunk))
	print("chunk_x")
	chunk_x = chunk[0]
	print(type(chunk_x))

