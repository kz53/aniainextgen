import json

class Review:
    def __init__(self,
                 review_timestamp = "",
                 review_date = "",
                 review_helpful = "",
                 review_episodes_seen = "",
                 review_overall = "",
                 review_story = "",
                 review_animation = "",
                 review_sound = "",
                 review_character = "",
                 review_enjoyment = "",
                 review_text = "",
                 review_page = ""):
        self.review_timestamp = review_timestamp
        self.review_date = review_date
        self.review_helpful = review_helpful
        self.review_episodes_seen = review_episodes_seen
        self.review_overall = review_overall
        self.review_story = review_story
        self.review_animation = review_animation
        self.review_sound = review_sound
        self.review_character = review_character
        self.review_enjoyment = review_enjoyment
        self.review_text = review_text
        self.review_page = review_page

    def toJSON(self):
        return self.__dict__

