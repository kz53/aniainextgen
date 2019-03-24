import sys
import os
import csv
sys.path.insert(0, os.path.abspath('..'))
from Serializable.AnimeDocument import AnimeDocument
from Serializable.Review import Review
from Serializable.ModelToSerializable import ModelToSerializableConverter

"""
This is a script to convert the csv data (AnimeReviews.csv) to json serialized list.
"""


def makeAnimeDocuments(fileName, destName):
    animeDocuments = {}
    modelToSerializableConverter = ModelToSerializableConverter()
    with open(fileName, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            anime_id = row["anime_id"]
            if not anime_id.isdigit():
                print("Skipping: {}".format(anime_id))
                continue
            anime_id = int(anime_id)
            if anime_id not in animeDocuments:
                animeDocument = AnimeDocument()
                for key in list(row.keys()):
                    if not "anime_" in key:
                        continue
                    elif key == "anime_genres":
                        for genre in row[key].split('|'):
                            animeDocument.addGenre(genre.strip())
                    else:
                        value = row[key]
                        if value.strip().isdigit():
                            value = int(value.strip())
                        setattr(animeDocument, key, value)
                animeDocuments[anime_id] = animeDocument
            review = Review()
            for key in list(row.keys()):
                if "review_" in key:
                    value = row[key]
                    if value.strip().isdigit():
                        value = int(value.strip())
                    setattr(review, key, value)
            animeDocuments[anime_id].addReview(review)
    animeDocuments = sorted(animeDocuments.values(), key = lambda document: document.anime_id)
    for index, document in enumerate(animeDocuments):
        document.anime_index = index
    modelToSerializableConverter.dumpModel(destName, animeDocuments)

if len(sys.argv) < 3:
    print("Takes two command line arguments: 1) csv file with review data 2) destination file for json representation")
else:
    makeAnimeDocuments(sys.argv[1], sys.argv[2])
