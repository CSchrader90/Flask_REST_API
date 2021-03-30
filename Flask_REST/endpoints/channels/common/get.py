from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
def get(self, user, channel_name):
	"""Pass channel_name to get info for channel otherwise return list of all channels"""

	if channel_name is None:
		channel_objects = ChannelModel.query.filter_by(user=user.username).all()
		channel_name_list = [instance.channel for instance in channel_objects]
		channel_logger.info(f"Returning all channels in GET|[user:{user.username}]")
		return make_response({"channels": channel_name_list}, 200)

	result = ChannelModel.query.filter_by(user=user.username, channel=channel_name).first()
	if result is None:
		channel_logger.error(f"Channel does not exist in GET |[user:{user.username},channel:{channel}]")
		return make_response("Channel does not exist", 404)

	schema = ChannelSchema(many=False)
	output = schema.dump(result)
	channel_logger.info(f"Returning channel in GET|[channel:{channel},user: {user.username}]")
	return make_response(output, 200)
