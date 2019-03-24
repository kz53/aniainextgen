import json
from AnimeDocument import AnimeDocument
from Review import Review
from Genre import Genre

class SerializableToModelConverter:
    """
    Converts json serialized dictionaries to AnimeDocument objects
    """

    def convert(self, serialized_dict):
        """Converts a json string to an AnimeDocument object"""
        raise NotImplementedError("Let Cheyenne know if you want\n" + 
                                  "SerializableToModelConverter.convert implemented.\n" +
                                  "Use convertFromFile as alternative in the meanwhile")

    def convertFromFile(self, fileName):
        """Reads a json file and converts it to list of AnimeDocument objects"""
        with open(fileName, "r") as f:
            data = json.loads(f.readlines()[0], object_hook = self.convertAnimeDocument)
        return data 

    def convertAnimeDocument(self, serialized_dict):
        animeDocument = AnimeDocument()
        for key in serialized_dict:
            value = serialized_dict[key]
            if key == "anime_reviews":
                for review_dict in value:
                    review = self.convertReview(review_dict.__dict__)
                    animeDocument.addReview(review)
            elif key == "anime_genres":
                for genre_dict in value:
                    genre = self.convertGenre(genre_dict.__dict__)
                    animeDocument.addGenre(genre)
            else:
                setattr(animeDocument, key, value)
        return animeDocument
                            
    def convertReview(self, serialized_dict):
        review = Review()
        for key in serialized_dict:
            if "review_" in key:
                value = serialized_dict[key]
                setattr(review, key, value)
        return review 

    def convertGenre(self, serialized_dict):
        genre = Genre()
        for key in serialized_dict:
            if "genre_" in key:
                value = serialized_dict[key]
                setattr(genre, key, value)
        return genre
