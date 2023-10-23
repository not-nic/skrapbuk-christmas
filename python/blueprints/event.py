from flask import Blueprint, jsonify
from flask_discord import requires_authorization
from python.classes.models.user import User
from app import config, discord, database

event = Blueprint('event_blueprint', __name__, url_prefix='/event')

@event.route("/countdown")
@requires_authorization
@config.is_banned
def countdown():
    """
    return a countdown timer until skrapbuk starts.
    Returns:
         json object of the countdown.
    """
    return jsonify({"countdown": config.get_countdown()})

@event.route("/start")
@requires_authorization
@config.is_admin
def start():
    """
    Start the skrapbuk event by assigning partners if the config is set to False.
    This action can be overridden with the "/restart" endpoint.

    Returns:
        str: A message indicating skrapbuk has been started or a message informing the
        admin that it has already been initiated.
    """
    is_started = config.find_value('is_started')
    started_by = discord.fetch_user().username

    if not is_started:
        database.pair_users()
        config.update_value('is_started', True)
        return f"{started_by} has started the Skrapbuk-Christmas event!"
    else:
        return f"Skrapbuk event has already been started by {started_by}."

@event.route("/pairs")
@requires_authorization
@config.is_admin
def get_partners():
    """
    A function to show admins each user and their respective 'partner'.

    Returns:
        Json object of user information and their 'partner' information.
    """
    # Return all users with a partner
    users = User.query.filter(User.is_banned == False).all()
    user_partner_pairs = []
    # iterate over each user
    for user in users:
        # find the data about a partner
        partner_data = User.query.filter_by(snowflake=user.partner).first()
        # create dict with the user & partner data.
        user_data = {
            'snowflake' : user.snowflake,
            'username' : user.username,
            'partner' : {
                'snowflake' : partner_data.snowflake,
                'username' : partner_data.username
            }
        }
        user_partner_pairs.append(user_data)
    return jsonify(user_partner_pairs)