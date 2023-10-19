from flask import Blueprint, request
from flask_discord import requires_authorization
from app import database, config

ban = Blueprint('ban_blueprint', __name__)

@ban.route("/ban/<string:snowflake>", methods=['GET'])
@requires_authorization
@config.is_admin
def block(snowflake):
    reason = request.args.get('reason')
    return database.ban_user(snowflake, reason)

@ban.route("/unban/<string:snowflake>", methods=['GET'])
@requires_authorization
@config.is_admin
def unblock(snowflake):
    return database.unban_user(snowflake)