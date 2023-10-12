import os
from flask import Flask, redirect, jsonify, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from python.config import Config
from python.classes.database import Database
from python.classes.logging import Logging
from python.classes.user import User

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["DISCORD_CLIENT_ID"] = os.getenv('SB_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('SB_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:8080/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv('SB_BOT_TOKEN')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://nic:password@localhost:3306/skrapbuk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

discord = DiscordOAuth2Session(app)
logger = Logging()
config = Config('D:/Projects/skrapbuk-christmas/python/config.yml', logger)
logger.start_processing_thread()

database = Database(app)
# database.seed_data(10)

@app.route("/")
def login():
    return discord.create_session(scope=['identify', 'guilds'])

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(location="http://localhost:5173/profile")

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    # TODO: Make this function return the user to the login page from the frontend.
    ip_address = request.remote_addr
    endpoint = request.endpoint
    logger.queue_message(
        f"{ip_address} tried to access /{endpoint} but is currently unauthorised.",
        'ERROR'
    )

    return redirect(location="http://localhost:8080/")

@app.route("/countdown")
@requires_authorization
def countdown():
    return jsonify({"countdown": config.get_countdown()})

@app.route("/user")
@requires_authorization
def user_info():
    # get logged in user from flask
    flask_discord_user = discord.fetch_user()

    # create user with less info as @requires_authorisation does not check scopes.
    user = User(
        flask_discord_user.id,
        flask_discord_user.avatar_url,
        flask_discord_user.username,
        in_server(),
        is_admin()
    )

    return user.to_json()

@requires_authorization
def in_server() -> bool:
    # check if user is in the server
    return any(guild.id == config.find_value('server') for guild in discord.fetch_guilds())

@requires_authorization
def is_admin() -> bool:
    # check if user is an admin from config.yml
    return discord.fetch_user().id in config.get_admins()

@app.route("/join")
@requires_authorization
def join():
    # get logged in user from flask
    flask_discord_user = discord.fetch_user()

    # create user with less info as @requires_authorisation does not check scopes.
    new_user = User(
        flask_discord_user.id,
        flask_discord_user.avatar_url,
        flask_discord_user.username,
        in_server(),
        is_admin()
    )

    database.session.add(new_user)

    # - add dummy data along with user - #
    sample_user1 = User(snowflake='123', avatar_url='avatar1.jpg', username='user1', in_server=True, is_admin=True)
    sample_user2 = User(snowflake='456', avatar_url='avatar2.jpg', username='user2', in_server=True, is_admin=False)
    sample_user3 = User(snowflake='789', avatar_url='avatar3.jpg', username='user3', in_server=True, is_admin=False)
    database.session.add_all([sample_user1, sample_user2, sample_user3])
    database.session.commit()

    logger.queue_message(
        f"User {flask_discord_user.username} ({flask_discord_user.id}) has been added to the database.",
        'INFO'
    )

    return "Joined Skrapbuk Christmas"

@app.route("/start")
@requires_authorization
@config.is_admin
def start():
    # TODO: Implement functionality to pair users with another user
    return f"{discord.fetch_user().username} is an admin and can start the event"

@app.route("/users", methods=['GET'])
@requires_authorization
@config.is_admin
def all_users():
    total_users = len(User.query.all())
    return f"There are {total_users} users signed up."

if __name__ == "__main__":
    app.run()