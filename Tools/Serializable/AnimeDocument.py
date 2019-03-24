import json
from Review import Review
from Genre import Genre
from gensim.models.doc2vec import TaggedDocument
from nltk import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

class AnimeDocument:
    def __init__(self,
                 anime_index = "",
                 anime_id = "",
                 anime_english_title = "",
                 anime_japanese_title = "",
                 anime_image_url = "",
                 anime_genres = None,
                 anime_synopsis = "",
                 anime_rating_value = "",
                 anime_rating_count = "",
                 anime_rating = "",
                 anime_ranked = "",
                 anime_popularity = "",
                 anime_favorites = "",
                 anime_members = "",
                 anime_number_of_episodes = "",
                 anime_type = "",
                 anime_source = "",
                 anime_background = "",
                 anime_premiered = "",
                 anime_status = "",
                 anime_broadcast = "",
                 anime_producers = "",
                 anime_licensors = "",
                 anime_studios = "",
                 anime_duration = "",
                 anime_side_story = "",
                 anime_adaptation = "",
                 anime_summary = "",
                 anime_full_story = "",
                 anime_parent_story = "",
                 anime_sequel = "",
                 anime_prequel = "",
                 anime_alternative_setting = "",
                 anime_other = "",
                 anime_reviews = None):
        self.anime_index = anime_index
        self.anime_id = anime_id
        self.anime_english_title = anime_english_title
        self.anime_japanese_title = anime_japanese_title
        self.anime_image_url = anime_image_url
        if not anime_genres:
            anime_genres = []
        self.anime_genres = anime_genres
        self.anime_synopsis = anime_synopsis
        self.anime_rating_value = anime_rating_value
        self.anime_rating_count = anime_rating_count
        self.anime_rating = anime_rating
        self.anime_popularity = anime_popularity
        self.anime_favorites = anime_favorites
        self.anime_members = anime_members
        self.anime_number_of_episodes = anime_number_of_episodes
        self.anime_type = anime_type
        self.anime_source = anime_source
        self.anime_background = anime_background
        self.anime_premiered = anime_premiered
        self.anime_status = anime_status
        self.anime_broadcast = anime_broadcast
        self.anime_producers = anime_producers
        self.anime_licensors = anime_licensors
        self.anime_studios = anime_studios
        self.anime_duration = anime_duration
        self.anime_summary = anime_summary
        self.anime_full_story = anime_full_story
        self.anime_parent_story = anime_parent_story
        self.anime_sequel = anime_sequel
        self.anime_prequel = anime_prequel
        self.anime_alternative_setting = anime_alternative_setting
        self.anime_other = anime_other
        if not anime_reviews:
            anime_reviews = []
        self.anime_reviews = anime_reviews

    def addReview(self, review):
        """Adds a Review object to self.anime_reviews"""
        if isinstance(review, Review):
            if not any(other.__dict__ == review.__dict__ for other in self.anime_reviews):
                self.anime_reviews.append(review)
            else:
                print("DUPLICATE DICT")
        else:
            raise ValueError("object is not instance of Review")

    def addGenre(self, genre):
        """Adds a Genre object to self.anime_genres"""
        if isinstance(genre, Genre):
            pass
        elif isinstance(genre, str):
            try:
                genre_name = genre[:genre.index('(')].strip().lower().replace(' ', '_')
                genre_id = int(genre[genre.index('(')+1 : genre.index(')')])
            except:
                print("Error: incorrectly formatted genre {}.  Ignoring.".format(genre))
                return
            genre = Genre(genre_name = genre_name, genre_id = genre_id)
        if genre not in self.anime_genres:
            self.anime_genres.append(genre)

    def getAllReviewText(self):
        """Returns all review text concatenated with a space"""
        return " ".join([review.review_text for review in self.anime_reviews])

    def getGenreVector(self):
        """
        Returns a binary vector representing whether MAL tags the anime with
        a particular genre or not
        """
        genreDictionary = self.getGenreDictionary()
        sortedGenres = sorted(genreDictionary.items(), key = lambda tup : tup[0].genre_id)
        return [tup[1] for tup in sortedGenres]

    def getGenreDictionary(self):
        """
        Returns a binary dictionary for whether the anime is tagged with the
        MAL genre or not
        """
        genreDictionary = {}
        genres = [Genre(u'action', 1),
                  Genre(u'adventure', 2),
                  Genre(u'cars', 3),
                  Genre(u'comedy', 4),
                  Genre(u'dementia', 5),
                  Genre(u'demons', 6),
                  Genre(u'mystery', 7),
                  Genre(u'drama', 8),
                  Genre(u'ecchi', 9),
                  Genre(u'fantasy', 10),
                  Genre(u'game', 11),
                  Genre(u'hentai', 12),
                  Genre(u'historical', 13),
                  Genre(u'horror', 14),
                  Genre(u'kids', 15),
                  Genre(u'magic', 16),
                  Genre(u'martial_arts', 17),
                  Genre(u'mecha', 18),
                  Genre(u'music', 19),
                  Genre(u'parody', 20),
                  Genre(u'samurai', 21),
                  Genre(u'romance', 22),
                  Genre(u'school', 23),
                  Genre(u'sci-fi', 24),
                  Genre(u'shoujo', 25),
                  Genre(u'shoujo_ai', 26),
                  Genre(u'shounen', 27),
                  Genre(u'shounen_ai', 28),
                  Genre(u'space', 29),
                  Genre(u'sports', 30),
                  Genre(u'super_power', 31),
                  Genre(u'vampire', 32),
                  Genre(u'yaoi', 33),
                  Genre(u'yuri', 34),
                  Genre(u'harem', 35),
                  Genre(u'slice_of_life', 36),
                  Genre(u'supernatural', 37),
                  Genre(u'military', 38),
                  Genre(u'police', 39),
                  Genre(u'psychological', 40),
                  Genre(u'thriller', 41),
                  Genre(u'seinen', 42),
                  Genre(u'josei', 43)]
        for genre in genres:
            genreDictionary[genre] = 0
        for genre in self.anime_genres:
            genreDictionary[genre] = 1
        return genreDictionary

    def toTaggedDocument(self, option="review"):
        """Returns a TaggedDocument object with words equal to the list of tokens from the
        tokenized reviews (all concatenated).  The TaggedDocument tag is equal to 'anime_id_{{self.anime_id}}'.
        Stop word tokens are not included in the list of tokens.
        Note: this method is for use in gensim's Doc2Vec model."""
        tokenizer = RegexpTokenizer(r'\w+')
        englishStopwords = set(stopwords.words('english'))
        if option == "review":
            text = self.getAllReviewText().lower()
        elif option == "synopsis":
            text = self.anime_synopsis.lower()
        else:
            raise ValueError("Unknown option " + option + " in AnimeDocument.toTaggedDocument")
        tokens = [token for token in tokenizer.tokenize(text) if token not in englishStopwords]
        return TaggedDocument(tokens, ["anime_id_{}".format(self.anime_id)])

    def toJSON(self):
        dictionaryRepresentation = self.__dict__
        dictionaryRepresentation['anime_reviews'] = [review.toJSON() for review in self.anime_reviews]
        dictionaryRepresentation['anime_genres'] = [genre.toJSON() for genre in self.anime_genres]
        return dictionaryRepresentation
