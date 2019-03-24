import csv
import sys
import os
from gensim.models import Doc2Vec
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter

converter = SerializableToModelConverter()
serializedJsonFileName = sys.argv[1] #just get it from command line arguments
data = converter.convertFromFile(serializedJsonFileName)

# USING REVIEW DATA
taggedDocuments = []
for animeDocument in data:
    taggedDocuments.append(animeDocument.toTaggedDocument(option="review"))
model = Doc2Vec(vector_size=300, window=20, min_count=5, alpha=0.025, min_alpha=0.025, workers=4)
model.build_vocab(taggedDocuments)
print("done building vocab review")
model.train(taggedDocuments, total_examples=model.corpus_count, epochs=model.iter)
model.save('../../data/doc2vecreview.model')

# USING SYNOPSIS DATA
taggedDocuments = []
for animeDocument in data:
    taggedDocuments.append(animeDocument.toTaggedDocument(option="synopsis"))
model = Doc2Vec(vector_size=300, window=20, min_count=5, alpha=0.025, min_alpha=0.025, workers=4)
model.build_vocab(taggedDocuments)
print("done building vocab synopsis")
model.train(taggedDocuments, total_examples=model.corpus_count, epochs=model.iter)
model.save('../../data/doc2vecsynopsis.model')
