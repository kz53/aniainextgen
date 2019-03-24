import json

class Genre:
    def __init__(self,
                 genre_name = "",
                 genre_id = ""):
        self.genre_id = genre_id
        self.genre_name = genre_name

    def __eq__(self, other):
        if isinstance(other, Genre):
            return self.genre_id == other.genre_id and self.genre_name == other.genre_name
        return False

    def __hash__(self):
        return hash((self.genre_id, self.genre_name))

    def toJSON(self):
        return self.__dict__

