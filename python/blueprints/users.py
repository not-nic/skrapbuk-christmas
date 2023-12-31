import os

from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from flask_discord import requires_authorization
from python.classes.models.user import User
from python.classes.models.answers import Answers
from python.classes.models.artwork import Artwork
from app import app, database, config, discord, logger

users = Blueprint('users_blueprint', __name__, url_prefix='/users')

ALLOWED_FORMATS = {"png", "jpg", "jpeg", "gif", "mp3", "mp4"}
# Define the maximum file size (in bytes) (default 50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

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

    # check if a user has filled in every question, error if any are empty.
    empty_answers = [field for field in required_fields if not data.get(field)]
    if empty_answers:
        return jsonify({"error": f"The following answers are empty: {', '.join(empty_answers)}."}), 400

    # check if any answers exceeds 280 characters.
    exceeding_answers = [field for field in required_fields if len(str(data[field])) > 280]
    if exceeding_answers:
        return jsonify({"error": f"The following answers exceed the character limit:"
                                 f" {', '.join(exceeding_answers)}."}), 400

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

@users.route("/answers", methods=['GET'])
@requires_authorization
@config.created_answers
@config.is_banned
def get_answers(snowflake=None):
    """
    Get answers from the database based on snowflake.
    (used within '/partner' endpoint to get partner answers)
    :param snowflake: Discord snowflake.
    Returns:
        (dict/json) object of users answers.
    """
    if snowflake is None:
        user_snowflake = discord.fetch_user().id
    else:
        user_snowflake = snowflake

    user_answers = Answers.query.filter_by(user_snowflake=user_snowflake).first()
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

    if request.method == 'GET':
        return jsonify({"error": "oh no! we couldn't find those answers, have you created them?"}), 400
    else:
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
                                  f"Check the countdown to see how long until you can start!",
                        "joined" : True
                        }), 400

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

    return jsonify({"message": f"Thanks {username} for signing up to Skrapbuk Christmas! "
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
    partner = User.query.filter_by(snowflake=partner_snowflake).first()

    # return limited information about the partner i.e. discord snowflake, username and avatar url.
    partner_info = {
        'snowflake' : partner.snowflake,
        'username' : partner.username,
        'avatar_url' : partner.avatar_url,
    }

    return jsonify({
        "details" : partner_info,
        "answers" : get_answers(snowflake=partner_snowflake)
    })

@users.route("/upload", methods=['POST'])
@requires_authorization
@config.is_banned
@config.has_partner
def upload_artwork():
    """
    Endpoint to handle artwork uploads during the event.
    Returns:
        (json) message if the file is uploaded successfully or unsuccessfully.
    """
    # check if request has a file part
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    original_filename = file.filename

    # check if the filename is blank
    if original_filename == "":
        return jsonify({"error": "No file selected."}), 400

    # if the file exists, and is in an accepted image format .gif, .png, etc...
    if file and accepted_image_format(original_filename):
        user = User.query.filter_by(snowflake=discord.fetch_user().id).first()

        # If a support file format, check the file size in memory.
        file_size = getattr(file, 'content_length', 0) or len(file.read())
        file.seek(0)  # Reset the file cursor

        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds the maximum allowed size. (max 50MB)"}), 400

        # check if the user exists
        if user:
            # get the partner and set a new filename
            partner = User.query.filter_by(snowflake=user.partner).first()
            new_filename = f"{user.username}_{partner.username}_{generate_timestamp(original_filename)}"

            # check if the user has already submitted artwork and update it.
            handle_existing_artwork(user, new_filename)
            save_file(file, new_filename)

            return jsonify({"message": "Artwork Uploaded Successfully."}), 200

        return jsonify({"error": "User not found."}), 400
    else:
        extension = original_filename.rsplit(".", 1)[-1]
        allowed_formats_str = ', '.join(ALLOWED_FORMATS)
        return jsonify({"error": f"Oops! We don't support the '{extension}' file extension. "
                                 f"the supported file formats are: [{allowed_formats_str.upper()}]"}), 400

def handle_existing_artwork(user, filename):
    """
    Handle users who have already submitted artwork by deleting the existing file
    and replacing it with the new file.
    :param user: the user who is attempting to replace the file.
    :param filename: filename of the new file.
    """
    existing_artwork = Artwork.query.filter_by(created_by=user.snowflake).first()
    if existing_artwork:
        existing_file_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_artwork.image_path)

        if os.path.exists(existing_file_path):
            os.remove(existing_file_path)

        database.update_existing_artwork(existing_artwork, filename)
    else:
        database.create_artwork_entry(user, filename)

def save_file(file, new_filename):
    """
    Function to save file / artwork to the file system.
    :param file: The file to be saved.
    :param new_filename: the file's filename.
    """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    file.save(filepath)

def generate_timestamp(filename):
    """
    Generate a timestamp for the file, keeping its existing extension.
    :param filename to get extension from.
    Returns:
        string of timestamp and file extension e.g. 01112023005121.png
    """
    timestamp = datetime.now().strftime('%d%m%Y%H%M%S')
    file_extension = os.path.splitext(filename)
    return f'{timestamp}{file_extension[1]}'

def accepted_image_format(filename) -> bool:
    """
    Return boolean if the file is / is not in the ALLOWED_FORMATS list.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_FORMATS

@users.route("/artwork", methods=["GET"])
@requires_authorization
@config.is_banned
@config.has_partner
def uploaded_file():
    """
    If the user is not banned & has a partner, display the image they have uploaded.
    This endpoint does not show the artwork created for them, instead the artwork they have created.
    Returns:
        (file) if the artwork exists return the image/file.
        (json) error message indicating the user or artwork doesn't exist.
    """
    snowflake = discord.fetch_user().id
    user = User.query.filter_by(snowflake=snowflake).first()

    if user:
        user_artwork = Artwork.query.filter_by(created_by=user.snowflake).first()

        if user_artwork:
            return send_from_directory(app.config['UPLOAD_FOLDER'], user_artwork.image_path), 200
        else:
            return jsonify({"error": f"You've not uploaded any artwork yet!"}), 400

    else:
        return jsonify({"error": f"User ({snowflake}) has not joined the event."}), 400

@users.route("/all", methods=["GET"])
@requires_authorization
@config.is_admin
def all_users():
    """
    Function for admins to get all the users from the database and return them as a Json object.
    """
    return database.get_all_users()

@users.route("/artwork/<snowflake>", methods=["GET"])
@requires_authorization
@config.is_admin
def get_artwork_from_id(snowflake):
    """
    Function to allow admins to get the artwork of a user based on their snowflake.
    :param snowflake: discord snowflake.
    Returns:
        (file) if successful the uploaded file for the desired user.
        (json) response error response message.
    """
    user = User.query.filter_by(snowflake=snowflake).first()
    if user:
        artwork = Artwork.query.filter_by(created_by=user.snowflake).first()
        if artwork:
            return send_from_directory(app.config['UPLOAD_FOLDER'], artwork.image_path)
        else:
            return jsonify({"error": f"No artwork for user {user.snowflake}"}), 400
    else:
        return jsonify({"error": f"No user with {snowflake} snowflake."}), 400