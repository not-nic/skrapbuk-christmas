import random, string

from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
database = SQLAlchemy()

from python.classes.models.user import User
from python.classes.logging import Logging
from python.classes.models.ban_list import BanList

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
        function to return the current database session.
        Returns:
             Current database session.
        """
        return self.db.session

    def add_user(self, user):
        """
        wrapper function to add a user to the database.
        :param user: the user object to be added.
        """
        self.get_session().add(user)
        self.get_session().commit()

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
            self.get_session().add_all(generated_users)
            self.get_session().commit()

            # add notification message to the log.
            logger.queue_message(f"Created and inserted {seed_amount} dummy users to the database.",
                                 'CREATED')

    def get_all_users(self):
        """
        Get all signed-up users from user table.
        Returns:
            (json) list of users as json objects.
        """
        with self.app.app_context():
            users = User.query.all()
            return [user.to_json() for user in users]

    def ban_user(self, snowflake, reason):
        """
        Ban a toxic user by adding their id to a ban_list table and adding an is_banned flag to their
        database entry.
        :param snowflake: Discord snowflake ID.
        :param reason: a reason for the ban.
        Returns:
            (json) A message informing that the user has either been banned or not found.
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
                return jsonify({"message": f"User ({snowflake}) is already banned."}), 200


            # user not already banned, ban the user.
            banned_user.is_banned = True
            ban_entry = BanList(
                user_snowflake=banned_user_snowflake,
                reason=reason,
                banned_user=banned_user
            )

            self.get_session().add(ban_entry)
            self.get_session().commit()

            return jsonify({"message": f"User ({snowflake}) has been banned."}), 200
        else:
            return jsonify({"error": f"User ({snowflake}) not found."}), 400

    def unban_user(self, snowflake):
        """
        Unban a user from their snowflake
        :param snowflake: id of the user to be unbanned.
        Returns:
            (json) A message informing the user has been unbanned, or not found.
        """
        banned_user = User.query.filter_by(snowflake=snowflake).first()

        # check if the user exists
        if banned_user:

            # set banned flag to false
            banned_user_snowflake = banned_user.snowflake
            banned_user.is_banned = False

            ban_list_entry = BanList.query.filter_by(user_snowflake=banned_user_snowflake).first()
            # if user is found in the ban list, remove them
            if ban_list_entry:
                self.get_session().delete(ban_list_entry)
                self.get_session().commit()
                return jsonify({"message": f"User ({snowflake}) has been unbanned."}), 200
            else:
                return jsonify({"message": f"User ({snowflake}) is not banned."}), 200
        else:
            return jsonify({"error": f"User ({snowflake}) not found."}), 400

    def pair_users(self):
        """
        'pair' all the users that have signed up to the skrapbuk event, by randomly assigning them a 'partner'.
        """
        # get all unbanned users & shuffle them.
        users = User.query.filter(User.is_banned == False).all()
        random.shuffle(users)

        num_users = len(users)

        logger.queue_message(f"Starting to pair users", 'INFO')

        # iterate over all users
        for i in range(num_users):

            # calculate the index of the 'partner' creating a pseudo-circular linked list
            partner = (i + 1) % num_users
            # assign the partner to the current user
            users[i].partner = users[partner].snowflake

            self.get_session().commit()

            logger.queue_message(f"{users[i].username} ({users[i].snowflake}) -> "
                                 f"{users[partner].username} ({users[partner].snowflake})", 'INFO')

        logger.queue_message(f"Finished pairing users.", 'INFO')



