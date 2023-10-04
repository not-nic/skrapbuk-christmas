import json
from python.config import Config

config = Config('D:/Projects/skrapbuk-christmas/python/config.yml')

class User:
    def __init__(self, snowflake, avatar_url, username, in_server, is_admin):
        self.snowflake = snowflake
        self.avatar_url = avatar_url
        self.username = username
        self.in_server = in_server
        self.is_admin = is_admin

    def to_json(self):
        return json.dumps(self.__dict__)

