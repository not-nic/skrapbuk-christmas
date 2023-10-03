import os
from datetime import datetime
from flask import Flask, redirect, url_for, jsonify
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from classes.user import User

app = Flask(__name__)

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

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("/"))

@app.route("/time")
@requires_authorization
def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify({"the_time": f"{current_time}"})

@app.route("/user")
@requires_authorization
def user_info():

    # get logged in user from flask
    flask_discord_user = discord.fetch_user()

    # create user with less info as @requires_authorisation does not check scopes.
    user = User(
        flask_discord_user.id,
        flask_discord_user.avatar_url,
        flask_discord_user.username
    )

    return user.to_json()

if __name__ == "__main__":
    app.run()
