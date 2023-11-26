import yaml
import time

from functools import wraps
from flask_discord import DiscordOAuth2Session
from flask import request, jsonify
from python.classes.models.user import User
from python.classes.models.ban_list import BanList
from python.classes.models.answers import Answers

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
        """
        Find value in the 'discord' property of config.yml return it value.
        :param key: Key of the value to be returned.

        Returns:
            (any) the value of the specified key.
        """
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
        """
        Get all admins from the discord property of config.yml
        Returns:
            (list) All admins in config.yml
        """
        return list(self.config.get('discord', {}).get('admins', {}).values())

    def get_countdown(self):
        """
        Gets a Days, Hours, Minutes, Seconds countdown from the skrapbuk event start time in config.yml.
        Returns:
            (str) Formatted string of the countdown until the event starts.
        """
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
        """
        Decorator function to check if a user is an admin.
        Returns:
            (nothing) continues with the function if the user is an admin.
            (abort) 401: Unauthorised message if the user is not an admin.
        """
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

                return jsonify({"error": "woah there, you're not an admin you can't view this content!"}), 401

        return wrapper

    def is_banned(self, func):
        """
        Decorator function to check if a user is banned from Skrapbuk.
        Returns:
            (nothing) continues with the function if the user not banned.
            (abort) 403: Forbidden message if the user is banned.
        """
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

                return jsonify({ "error": "You are banned, you cannot take part in Skrapbuk." }), 403

        return wrapper

    def has_partner(self, func):
        """
        Decorator Function to check if a user has been assigned a partner.
        Returns:
            (nothing) continues with the function if the user has a partner.
            (abort) 403: User is forbidden from viewing content as they do not have a partner.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            discord = DiscordOAuth2Session()
            snowflake = discord.fetch_user().id
            user = User.query.filter_by(snowflake=snowflake).first()

            # check if the user exists and has a partner
            if user and user.partner:
                 return func(*args, **kwargs)
            else:
                self.logger.queue_message(
                    message=f"{discord.fetch_user().username} ({discord.fetch_user().id}) does not have a partner",
                    message_type="INFO"
                )

                return jsonify({ "error" : f"User ({snowflake}) does not have a partner" }), 400

        return wrapper

    def created_answers(self, func):
        """
        Decorator function to check if a user has filled out their questions before trying to join skrapbuk.
        Returns:
            (nothing) continues with the function if the user has a partner.
            (abort) 403: Prompt user to fill out questions, before allowing them to join skrapbuk.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            discord = DiscordOAuth2Session()
            snowflake = discord.fetch_user().id
            username = discord.fetch_user().username
            user_answers = Answers.query.filter_by(user_snowflake=snowflake).first()

            # check if user answers exist.
            if user_answers:
                return func(*args, **kwargs)
            else:
                self.logger.queue_message(
                    message=f"{discord.fetch_user().username} ({discord.fetch_user().id}) has not answered questions.",
                    message_type="INFO"
                )

                return jsonify({ "error" : f"{username} ({snowflake}) you have not answered the questions."
                                           f" Please answer all questions to join skrapbuk!" }), 400

        return wrapper


