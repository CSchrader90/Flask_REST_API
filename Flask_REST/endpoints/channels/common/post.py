from flask import jsonify, make_response, request

from Flask_REST.caching.caching import cache, cache_key
from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token
from Flask_REST.endpoints.request_checks.checkForJsonBody import verify_json

@verify_token
@verify_json(logger=channel_logger, verb="POST", required_field="channel_name")
@cache.cached(key_prefix=cache_key)
def post(self, user, channel_name):
	"""Add a new channel"""

	request_args = request.get_json()

	channel_exists = ChannelModel.query.filter_by(user=user.username, channel=request_args["channel_name"]).first()
	if channel_exists:
		channel_logger.info(f"Channel already exists in POST|[channel:{request_args['channel_name']},user:{user.username}]")
		return make_response("Channel already exists", 400)

	new_channel_object = ChannelModel(user=user.username, channel=request_args["channel_name"])
	db.session.add(new_channel_object)
	db.session.commit()

	channel_logger.info(f"New channel created successfully in POST|[channel: {request_args['channel_name']},user:{user.username}]")
	return make_response("New channel created successfully", 201)
