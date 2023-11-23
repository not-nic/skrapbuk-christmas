from sqlalchemy import Column, Integer, String, Text
from python.classes.database import database

class Answers(database.Model):
    id = Column(Integer, primary_key=True)
    user_snowflake = Column(String(255))
    fav_game = Column(Text)
    fav_colour = Column(Text)
    fav_song = Column(Text)
    fav_film = Column(Text)
    fav_food = Column(Text)
    hobby_interest = Column(Text)

    def __init__(self, user_snowflake, fav_game, fav_colour, fav_song,
                fav_film, fav_food, hobby_interest):
        self.user_snowflake = user_snowflake
        self.fav_game = fav_game
        self.fav_colour = fav_colour
        self.fav_song = fav_song
        self.fav_film = fav_film
        self.fav_food = fav_food
        self.hobby_interest = hobby_interest

    def __str__(self):
        return (f"User snowflake answers:\n"
                f"Favourite Game: {self.fav_game}\n"
                f"Favourite Colour: {self.fav_colour}\n"
                f"Favourite Song: {self.fav_song}\n"
                f"Favourite Food: {self.fav_food}\n"
                f"Hobbies / Interests: {self.hobby_interest}")

    def to_json(self):
        return {
            'game': self.fav_game,
            'colour': self.fav_colour,
            'song': self.fav_song,
            'food': self.fav_food,
            'hobbies': self.hobby_interest,
        }