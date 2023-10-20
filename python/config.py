import yaml
import time

from functools import wraps
from flask_discord import DiscordOAuth2Session
from flask import abort, request
from python.classes.models.ban_list import BanList

class Config:
    def __init__(self, file_path, logger):
        self.file_path = file_path
        self.logger = logger

        with open(self.file_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def save_config(self):
        """
        Write changes & make updates to the config file.
        """
        with open(self.file_path, 'w') as file:
            yaml.dump(self.config, file)

    def find_value(self, key):
        return self.config.get('discord', {}).get(key, None)

    def update_value(self, key, new_value):
        """
        Update a value under the 'discord' property of config.yml.
        :param key: of the value to be updated.
        :param new_value: value to replace the one specified in the config.
        """
        self.config['discord'][key] = new_value
        self.save_config()

    def get_admins(self):
        return list(self.config.get('discord', {}).get('admins', {}).values())

    def get_countdown(self):
        current_time = int(time.time())
        time_difference = max(self.find_value('start_time') - current_time, 0)

        days = time_difference // (24 * 3600)
        time_difference %= (24 * 3600)
        hours = time_difference // 3600
        time_difference %= 3600
        minutes = time_difference // 60
        seconds = time_difference % 60

        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    def is_admin(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            discord = DiscordOAuth2Session()
            if discord.fetch_user().id in self.get_admins():
                return func(*args, **kwargs)
            else:
                self.logger.queue_message(
                    message=f"{discord.fetch_user().username} ({discord.fetch_user().id}) can't view /{request.endpoint}, "
                            f"only admins can access this function.",
                    message_type="INFO"
                )

                return abort(code=401)
        return wrapper

    def is_banned(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            discord = DiscordOAuth2Session()
            banned_user = BanList.query.filter_by(user_snowflake=discord.fetch_user().id).first()

            if not banned_user:
               return func(*args, **kwargs)
            else:
                self.logger.queue_message(
                    message=f"{discord.fetch_user().username} ({discord.fetch_user().id}) can't view /{request.endpoint}, "
                            f"because they are banned.",
                    message_type="INFO"
                )
                return f"You are banned, you cannot take part in Skrapbuk."

        return wrapper