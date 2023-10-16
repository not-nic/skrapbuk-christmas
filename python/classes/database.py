import random, string

from flask_sqlalchemy import SQLAlchemy
database = SQLAlchemy()

from python.classes.user import User
from python.classes.logging import Logging
from python.classes.ban_list import BanList

logger = Logging()

class Database:
    def __init__(self, app=None):
        self.db = database
        self.db.init_app(app)
        self.app = app
        # create user table on flask startup.
        with app.app_context():
            self.db.create_all()

    def get_session(self):
        """
        function to return the current 'shared' database session.
        :return: current database session
        """
        return self.db.session

    def add_user(self, user):
        """
        wrapper function to add a user to the database.
        :param user: the user object to be added.
        """
        self.db.session.add(user)

    def seed_data(self, seed_amount):
        """
        Generate dummy data for the database, including a snowflake, name and booleans to if they are admin
        or in the server.
        :param seed_amount: Amount of dummy users to be created (e.g. 5).
        """
        with self.app.app_context():
            generated_users = []

            for i in range(seed_amount):
                # Generate 18 digit snowflake (same length as discord)
                random_snowflake = random.randint(10**17, 10**18 - 1)
                # create a random 'username' from ascii letters (e.g. fxdlzMyP)
                random_name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
                random_avatar = f"avatar_{random_name}.jpg"
                random_boolean = random.choice([True, False])

                seed_user = User(
                    snowflake=random_snowflake,
                    avatar_url=random_avatar,
                    username=random_name,
                    in_server=random_boolean,
                    is_admin=random_boolean
                )

                generated_users.append(seed_user)
                # Debug Print: print(f"Random User: {random_name} ({random_snowflake}) {random_avatar}")

            # add and commit users to the database session.
            self.db.session.add_all(generated_users)
            self.db.session.commit()

            # add notification message to the log.
            logger.queue_message(f"Created and inserted {seed_amount} dummy users to the database.", 'CREATED')

    def get_all_users(self):
        """
        If the user is an admin, get all current signed-up users.
        :return: A json object of the signed-up users.
        """
        with self.app.app_context():
            users = User.query.all()
            return [user.to_json() for user in users]

    def get_user_by_snowflake(self, snowflake):
        """
        get a user by their snowflake.
        :param snowflake: discord id/snowflake.
        :return the user object.
        """
        with self.app.app_context():
            return User.query.get(snowflake=snowflake)

    def ban_user(self, snowflake, reason):
        """
        Ban a toxic user by adding their id to a ban_list table and adding an is_banned flag to their
        database entry.
        :param snowflake: Discord snowflake ID.
        :param reason: a reason for the ban.
        :return: A message informing that the user has either been banned or not found.
        """
        banned_user = User.query.filter_by(snowflake=snowflake).first()
        banned_user_snowflake = banned_user.snowflake

        if reason is None:
            reason = "No Reason"

        # check if the user exists
        if banned_user:

            # check if the user is already banned
            existing_ban = BanList.query.filter_by(user_snowflake=snowflake).first()
            if existing_ban:
                return f'User ({snowflake}) is already banned.'

            # user not already banned, ban the user.
            banned_user.is_banned = True
            ban_entry = BanList(
                user_snowflake=banned_user_snowflake,
                reason=reason,
                banned_user=banned_user
            )

            self.get_session().add(ban_entry)
            self.get_session().commit()

            return f'User ({snowflake}) has been banned.'
        else:
            return f'User ({snowflake}) not found.'
