from AnimeDocument import AnimeDocument
import json

class AnimeDocumentEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        return json.JSONEncoder.default(self, obj)

class ModelToSerializableConverter:
    """
    Converts AnimeDocument objects to a json serializabled format.
    """
    def convert(self, animeDocuments):
        """Converts list of AnimeDocument objects to a json serializable string"""
        return json.dumps(animeDocuments, cls=AnimeDocumentEncoder)

    def dumpSerialized(self, fileName, serializedAnimeDocuments):
        """Dumps a json serializable string to a file (overrides all file contents)"""
        with open(fileName, "w+") as jsonFile:
            json.dump(serializedAnimeDocuments, jsonFile)

    def dumpModel(self, fileName, animeDocuments):
        """Dumps a list of AnimeDocument objects to a file (overrides all file contents)"""
        with open(fileName, "w+") as jsonFile:
            json.dump(animeDocuments, jsonFile, cls=AnimeDocumentEncoder)

