from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db
from Logging.loggers import channel_logger
from Flask_REST.authorization.auth import verify_token

@verify_token
def delete(self, user, channel_name):
	"""Delete channel"""

	if channel_name is None:
		channel_logger.error(f"Channel name not provided in DELETE|[channel:<none>]")
		return make_response("Channel name not provided", 404)
	
	channel_result = ChannelModel.query.filter_by(user=user.username, channel=channel_name).first()
	if channel_result is None:
		channel_logger.error(f"Channel name does not exist in DELETE|[channel:{channel_name}]")
		return make_response("Channel does not exist", 404)
		
	db.session.delete(channel_result)
	db.session.commit()
	channel_logger.info(f"Channel successfully deleted in DELETE|[channel:{channel_name}]")
	return make_response("Channel successfully deleted", 200)
