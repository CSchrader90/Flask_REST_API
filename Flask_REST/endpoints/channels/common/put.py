from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token


@verify_token
def put(self, user, channel_name):
	"""Update a channels name """

	old_channel_name = channel_name # from query string
	if old_channel_name is None:
		return make_response("Channel name not provided", 400)

	if not request.is_json:
		return make_response("Missing request JSON body", 400)

	if "channel_name" not in request.get_json():
		return make_response("No updated name provided in JSON body", 400)

	new_channel_name = request.get_json()["channel_name"] # from JSON body

	channel_exists = ChannelModel.query.filter_by(user=user.username, 
												  channel=old_channel_name).first()
	if not channel_exists:
		return make_response("Channel doesn't exist", 404)
	db.session.delete(channel_exists)

	new_channel = ChannelModel(user=user.username, channel=new_channel_name)
	db.session.add(new_channel)
	db.session.commit()
	return make_response("Channel name updated", 200)
