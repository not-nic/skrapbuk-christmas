from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from python.classes.database import database

class User(database.Model):
    id = Column(Integer, primary_key=True)
    snowflake = Column(String(255), index=True)
    avatar_url = Column(String(255))
    username = Column(String(255))
    partner = Column(String(255), ForeignKey('user.snowflake'), nullable=True, default=None)
    in_server = Column(Boolean)
    is_admin = Column(Boolean)
    is_banned = Column(Boolean, default=False)

    def __init__(self, snowflake, avatar_url, username, in_server, is_admin):
        self.snowflake = snowflake
        self.avatar_url = avatar_url
        self.username = username
        self.in_server = in_server
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.snowflake} ({self.username})"

    def to_json(self):
        user_json = {
            'snowflake': self.snowflake,
            'avatar_url': self.avatar_url,
            'username': self.username,
            'partner': self.partner,
            'in_server': self.in_server,
            'is_admin': self.is_admin,
            'is_banned' : self.is_banned
        }
        return user_json