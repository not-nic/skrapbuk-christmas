from flask import Blueprint, request, jsonify
from flask_discord import requires_authorization
from python.classes.models.user import User
from python.classes.models.question import Question
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

@users.route("/questions", methods=['POST'])
@requires_authorization
@config.is_banned
def set_answers():
    data = request.get_json()

    # check if json is in acceptable format.
    required_fields = ['game', 'colour', 'song', 'film', 'food', 'hobby']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required JSON fields.'}), 400

    username = discord.fetch_user().username
    user_snowflake = discord.fetch_user().id

    # check if answers already exist, if so update them.
    if update_answers(user_snowflake, data):
        return jsonify({'message': f'Answers have been updated.'}), 200

    # answers didn't exist, create new row in question table and save them.
    user_answers = Question(
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

    return jsonify({'message': f"Thanks {username} we've saved your questions."}), 200

def update_answers(snowflake, data) -> bool:
    user_answers = Question.query.filter_by(user_snowflake=snowflake).first()
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
    user_answers = Question.query.filter_by(user_snowflake=snowflake).first()
    if user_answers:
        questions_json = {
            'game': user_answers.fav_game,
            'colour': user_answers.fav_colour,
            'song': user_answers.fav_song,
            'film': user_answers.fav_film,
            'food': user_answers.fav_food,
            'hobby': user_answers.hobby_interest
        }
        return questions_json
    return {}

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

@users.route("/partner", methods=['GET'])
@requires_authorization
@config.has_partner
def partner_info():
    snowflake = discord.fetch_user().id
    username = discord.fetch_user().username
    partner_snowflake = User.query.filter_by(snowflake=snowflake).first().partner
    partner_username =  User.query.filter_by(snowflake=partner_snowflake).first().username
    return (f"{username} your partner is {partner_username}. \n"
            f"{get_answers(partner_snowflake)}")