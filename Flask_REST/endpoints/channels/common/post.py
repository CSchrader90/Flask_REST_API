from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
def post(self, user, channel_name):
	"""Add a new channel"""

	if not request.is_json:
		return make_response("Bad request (not JSON)", 400)

	request_args = request.get_json()

	if "channel_name" not in request_args:
		return make_response("Channel name not provided", 404)
	channel_exists = ChannelModel.query.filter_by(user=user.username, 
												  channel=request_args["channel_name"]).first()
	if channel_exists:
		return make_response("Channel already exists", 400)
	
	new_channel_object = ChannelModel(user=user.username, channel=request_args["channel_name"])
	db.session.add(new_channel_object)
	db.session.commit()

	return make_response("New channel created successfully", 201)
