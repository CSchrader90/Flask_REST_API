from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db

def get(self):
	"""Pass channel_name to get info for channel otherwise return list of all channels"""

	request_args = request.args
	if "channel_name" not in request_args:
		channel_objects = ChannelModel.query.all()
		channel_name_list = [instance.channel for instance in channel_objects]
		return make_response({"channels": channel_name_list}, 200)

	result = ChannelModel.query.filter_by(channel=request_args["channel_name"]).first()
	if result is None:
		return make_response("Channel does not exist", 404)

	schema = ChannelSchema(many=False)
	output = schema.dump(result)
	return make_response(output, 200)
