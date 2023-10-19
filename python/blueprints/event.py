from flask import Blueprint, jsonify
from flask_discord import requires_authorization
from app import config, discord, database

event = Blueprint('event_blueprint', __name__, url_prefix='/event')

@event.route("/countdown")
@requires_authorization
@config.is_banned
def countdown():
    return jsonify({"countdown": config.get_countdown()})

@event.route("/start")
@requires_authorization
@config.is_admin
def start():
    # TODO: Implement functionality to pair users with another user
    database.pair_users(discord.fetch_user().id)
    return f"{discord.fetch_user().username} is an admin and can start the event"