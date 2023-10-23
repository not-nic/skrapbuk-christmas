from flask import Blueprint
from flask_discord import requires_authorization
from python.classes.models.user import User
from app import database, config, discord, logger

users = Blueprint('users_blueprint', __name__, url_prefix='/users')

@requires_authorization
def in_server() -> bool:
    # check if user is in the server
    return any(guild.id == config.find_value('server') for guild in discord.fetch_guilds())

@requires_authorization
def is_admin() -> bool:
    # check if user is an admin from config.yml
    return discord.fetch_user().id in config.get_admins()

@users.route("/me")
@requires_authorization
@config.is_banned
def user_info():
    # get logged in user from flask
    flask_discord_user = discord.fetch_user()

    # create user with less info as @requires_authorisation does not check scopes.
    user = User(
        flask_discord_user.id,
        flask_discord_user.avatar_url,
        flask_discord_user.username,
        in_server(),
        is_admin(),
    )

    return user.to_json()

@users.route("/join")
@requires_authorization
@config.is_banned
def join():

    # check if user has already joined event
    has_joined = User.query.filter_by(snowflake=discord.fetch_user().id).first()
    if has_joined:
        return "You have already joined skrapbuk, you can't join again 😩"

    # get logged in user from flask
    flask_discord_user = discord.fetch_user()

    # create user with less info as @requires_authorisation does not check scopes.
    new_user = User(
        snowflake=flask_discord_user.id,
        avatar_url=flask_discord_user.avatar_url,
        username=flask_discord_user.username,
        in_server=in_server(),
        is_admin=is_admin()
    )

    database.add_user(new_user)

    logger.queue_message(
        f"User {flask_discord_user.username} ({flask_discord_user.id}) has been added to the database.",
        'INFO'
    )

    return "Joined Skrapbuk Christmas"

@users.route("/all", methods=['GET'])
@requires_authorization
@config.is_admin
def all_users():
    return database.get_all_users()