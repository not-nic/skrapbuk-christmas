from sqlalchemy import Column, Integer, String, Text, ForeignKey
from python.classes.database import database

class BanList(database.Model):
    id = Column(Integer, primary_key=True)
    user_snowflake = Column(String(255), ForeignKey('user.snowflake'))
    reason = Column(Text)
    banned_user = database.relationship('User')

    def __init__(self, user_snowflake, reason, banned_user):
        self.user_snowflake = user_snowflake
        self.reason = reason
        self.banned_user = banned_user