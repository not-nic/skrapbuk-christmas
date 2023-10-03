import json
class User:
    def __init__(self, snowflake, avatar_url, username):
        self.snowflake = snowflake
        self.avatar_url = avatar_url
        self.username = username

    def to_json(self):
        return json.dumps(self.__dict__)