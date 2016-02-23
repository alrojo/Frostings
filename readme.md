#Frostings
Simple data loader for machine learning.

Couple your github.com/alrojo/Trifle with some Frostings!

#Documentation

This data loader is in four parts: LoadMethod, SampleGenerator, BatchGenerator, ChunkGenerator.

**LoadMethod**: Implements the loading of the data (sk.io.image for images, or maybe a wrapper for a database).
This class only has a skeleton is provided as it is often very different for different tasks. See the examples/europarl/text_loader.py for details on how to make a LoadMethod.

**SampleGenerator**: Handles repeating data (train repeat=True, valid and test repeat=False), shuffling (important for increasing types of mini-batches) and returns one sample, which is a tuple of elements. e.g. sample = (X, label) for one data point.

**BatchGenerator**: puts the data in a numpy array and packs it with other batch-level specifics (see examples/europarl/text_loader.py for details on a specific implementation)

**ChunkGenerator**: Gives a list of batches and computes chunk-level specifics such as zero-mean unit variance over a chunk (NOT supported yet)
