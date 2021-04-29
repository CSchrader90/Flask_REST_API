from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token
from Flask_REST.endpoints.request_checks.checkForJsonBody import verify_json


@verify_token
@verify_json(logger=channel_logger, verb="PUT", required_field="channel_name")
def put(self, user, channel_name):
	"""Update a channels name """

	old_channel_name = channel_name # from path parameter
	if old_channel_name is None:
		channel_logger.error(f"Failed to update channel (existing resource not provided in PUT|[channel:<none>,user:{user.username}]")
		return make_response("Channel name not provided", 400)

	new_channel_name = request.get_json()["channel_name"] # from JSON body

	channel_exists = ChannelModel.query.filter_by(user=user.username, 
												  channel=old_channel_name).first()
	if not channel_exists:
		channel_logger.error(f"Channel doesn't exist in PUT|[channel:{channel_name},user:{user.username}")
		return make_response("Channel doesn't exist", 404)
	db.session.delete(channel_exists)

	new_channel = ChannelModel(user=user.username, channel=new_channel_name)
	db.session.add(new_channel)
	db.session.commit()
	channel_logger.info(f"Channel updated in PUT|[channel {new_channel_name},user:{user.username}")
	return make_response("Channel name updated", 200)
