import os
from datetime import datetime
from flask import Flask, redirect, url_for, jsonify
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["SECRET_KEY"] = os.urandom(24)
app.config["DISCORD_CLIENT_ID"] = os.getenv('SB_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('SB_CLIENT_SECRET')
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:8080/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv('SB_BOT_TOKEN')

discord = DiscordOAuth2Session(app)

@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    # return redirect(url_for(".me"))
    return redirect(location="http://localhost:5173/callback")

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/")
def home():
    return f"Cool"

@app.route("/test")
@requires_authorization
def test():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify({"the_time": f"{current_time}"})

@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

if __name__ == "__main__":
    app.run()
