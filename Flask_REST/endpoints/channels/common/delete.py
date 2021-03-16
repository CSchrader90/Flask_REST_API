from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db

def delete(self):
	"""Delete channel"""

	request_args = request.args
	if "channel_name" not in request_args:
		return make_response("Channel name not provided", 404)
	
	channel_result = ChannelModel.query.filter_by(channel=request_args["channel_name"]).first()
	if channel_result is None:
		return make_response("Channel does not exist", 404)
		
	db.session.delete(channel_result)
	db.session.commit()
	return make_response("Channel successfully deleted", 200)
