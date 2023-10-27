import os

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_discord import requires_authorization
from python.classes.models.user import User
from python.classes.models.answers import Answers
from app import app, database, config, discord, logger

users = Blueprint('users_blueprint', __name__, url_prefix='/users')

@requires_authorization
def in_server() -> bool:
    # check if user is in the server
    return any(guild.id == config.find_value('server') for guild in discord.fetch_guilds())

@requires_authorization
def is_admin() -> bool:
    # check if user is an admin from config.yml
    return discord.fetch_user().id in config.get_admins()

@users.route("/me", methods=['GET'])
@requires_authorization
@config.is_banned
def user_info():
    """
    Function to get a logged-in user's discord information
    with a modified scope as a Json object.
    """
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

@users.route("/answers", methods=['POST'])
@requires_authorization
@config.is_banned
def set_answers():
    """
    Allow users to set their answers to the questions in the 'answers' database table.
    Returns:
        (json) Response message with success or failure based on the questions being created or updated.
    """
    data = request.get_json()

    # check if json is in acceptable format.
    required_fields = ['game', 'colour', 'song', 'film', 'food', 'hobby']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required JSON fields."}), 400

    username = discord.fetch_user().username
    user_snowflake = discord.fetch_user().id

    # check if answers already exist, if so update them.
    if update_answers(user_snowflake, data):
        return jsonify({"message": f"Answers have been updated."}), 200

    # answers didn't exist, create new row in answers table and save them.
    user_answers = Answers(
        user_snowflake=user_snowflake,
        fav_game=data['game'],
        fav_colour=data['colour'],
        fav_song=data['song'],
        fav_film=data['film'],
        fav_food=data['food'],
        hobby_interest=data['hobby']
    )

    database.get_session().add(user_answers)
    database.get_session().commit()

    return jsonify({"message": f"Thanks {username} we've saved your answers."}), 200

def update_answers(snowflake, data) -> bool:
    """
    Function to update questions answers if the user has already created  them.
    :param snowflake: discord snowflake.
    :param data: (json) data to update answers.

    Returns:
        (bool) returns a bool based on if the user was found and questions were updated.
    """
    user_answers = Answers.query.filter_by(user_snowflake=snowflake).first()
    if user_answers:
        user_answers.fav_game = data['game']
        user_answers.fav_colour = data['colour']
        user_answers.fav_song = data['song']
        user_answers.fav_film = data['film']
        user_answers.fav_food = data['food']
        user_answers.hobby_interest = data['hobby']
        database.get_session().commit()
        return True
    return False

def get_answers(snowflake) -> dict:
    """
    Get answers from the database based on snowflake.
    (used within '/partner' endpoint to get partner answers)
    :param snowflake: Discord snowflake.
    Returns:
        (dict/json) object of users answers.
    """
    user_answers = Answers.query.filter_by(user_snowflake=snowflake).first()
    if user_answers:
        answers_json = {
            'game': user_answers.fav_game,
            'colour': user_answers.fav_colour,
            'song': user_answers.fav_song,
            'film': user_answers.fav_film,
            'food': user_answers.fav_food,
            'hobby': user_answers.hobby_interest
        }
        return answers_json
    return {}

@users.route("/join")
@requires_authorization
@config.is_banned
@config.created_answers
def join():
    """
    Allows users to join the skrapbuk event if they are in the Gom's Garden discord server.
    Returns:
        (json) Success or failure response message based on if the user has joined the event.
    """
    username = discord.fetch_user().username
    snowflake = discord.fetch_user().id
    avatar_url = discord.fetch_user().avatar_url

    # check if user in server
    if not in_server:
        return jsonify({"error" : "You have to be part of the Gom's Garden server "
                                  "to join the skrapbuk christmas event."}), 400

    # check if user has already joined event
    has_joined = User.query.filter_by(snowflake=discord.fetch_user().id).first()
    if has_joined:
        return jsonify({"error" : f"Woah! {username} you are already in! "
                                  f"Check the countdown to see how long until you can start!"}), 400

    # create user with less info as @requires_authorisation does not check scopes.
    new_user = User(
        snowflake=snowflake,
        avatar_url=avatar_url,
        username=username,
        in_server=in_server(),
        is_admin=is_admin()
    )

    database.add_user(new_user)

    logger.queue_message(
        f"User {username} ({snowflake}) has been added to the database.",
        'INFO'
    )

    return jsonify({"message": f"Thanks {username} for signing up to Skrapbuk Christmas!"
                               f"Check the countdown to see when you can start!"}), 200

@users.route("/partner", methods=['GET'])
@requires_authorization
@config.is_banned
@config.has_partner
def user_partner():
    """
    Request a users partner information and answers to create artwork from.
    Returns:
        (json) object with partner info and answers.
    """
    snowflake = discord.fetch_user().id
    partner_snowflake = User.query.filter_by(snowflake=snowflake).first().partner
    partner =  User.query.filter_by(snowflake=partner_snowflake).first()

    # return limited information about the partner i.e. discord snowflake, username and avatar url.
    partner_info = {
        'snowflake' : partner.snowflake,
        'username' : partner.username,
        'avatar_url' : partner.avatar_url,
    }

    return jsonify({
        "partner" : partner_info,
        "answers" : get_answers(partner_snowflake)
    })

@users.route("/upload", methods=['POST'])
@requires_authorization
@config.is_banned
@config.has_partner
def upload_artwork():

    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    original_filename = file.filename

    if original_filename == "":
        return jsonify({"error": "No file selected."}), 400

    if file and accepted_image_format(original_filename):
        new_filename = f"{discord.fetch_user().id}_{generate_filename_timestamp(original_filename)}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        print(filepath)
        file.save(filepath)
        return jsonify({"message": "File Uploaded Successfully."}), 200
    else:
        extension = original_filename.rsplit(".", 1)[-1]
        print(f"'{extension}' is not a valid extension, Only use .png, .jpg, .jpeg, .gif!")
        return jsonify({"error": f"'{extension}' is not a valid extension, Only use .png, .jpg, .jpeg, .gif!"}), 400

def generate_filename_timestamp(filename):
    timestamp = datetime.now().strftime('%d%m%Y%H%M%S')
    file_extension = os.path.splitext(filename)
    return f'{timestamp}{file_extension[1]}'

def accepted_image_format(filename):
    allowed_formats = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_formats

@users.route("/all", methods=['GET'])
@requires_authorization
@config.is_admin
def all_users():
    """
    Function for admins to get all the users from the database and return them as a Json object.
    """
    return database.get_all_users()