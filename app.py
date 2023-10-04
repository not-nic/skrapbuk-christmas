import os
from datetime import datetime
from flask import Flask, redirect, url_for, jsonify
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from python.classes.user import User
from python.config import Config

app = Flask(__name__)

config = Config('D:/Projects/skrapbuk-christmas/python/config.yml')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["SECRET_KEY"] = os.urandom(24)
app.config["DISCORD_CLIENT_ID"] = os.getenv('SB_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('SB_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:8080/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv('SB_BOT_TOKEN')

discord = DiscordOAuth2Session(app)

@app.route("/")
def login():
    return discord.create_session(scope=['identify', 'guilds'])

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(location="http://localhost:5173/profile")

# TODO: Make this function return the user to the login page from the frontend.
@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    print(f"user is unauthorised {e}")
    return redirect(location="http://localhost:8080/")

@app.route("/countdown")
@requires_authorization
def time():
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

if __name__ == "__main__":
    app.run()
