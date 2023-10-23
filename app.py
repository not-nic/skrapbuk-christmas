import os
from flask import Flask, redirect, request
from flask_discord import DiscordOAuth2Session, Unauthorized
from python.classes.database import Database
from python.classes.logging import Logging
from python.config import Config

app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["DISCORD_CLIENT_ID"] = os.getenv('SB_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('SB_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:8080/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv('SB_BOT_TOKEN')
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://nic:password@localhost:3306/skrapbuk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = Database(app)
discord = DiscordOAuth2Session(app)
logger = Logging()
logger.start_processing_thread()
config = Config('D:/Projects/skrapbuk-christmas/python/config.yml', logger)

from python.blueprints import bans
from python.blueprints import event
from python.blueprints import users

app.register_blueprint(bans.ban)
app.register_blueprint(event.event)
app.register_blueprint(users.users)
# add seed data database.seed_data(10)

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

if __name__ == "__main__":
    app.run()