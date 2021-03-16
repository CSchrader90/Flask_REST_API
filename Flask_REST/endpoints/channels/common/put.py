from flask import jsonify, make_response, request

from Flask_REST.models.models import ChannelModel, ChannelSchema, db

def put(self):
	"""Update a channels name """

	if not request.is_json:
		return make_response("Missing request JSON body", 400)

	if "channel_name" not in request.get_json():
		return make_response("No updated name provided in JSON body", 400)

	new_channel_name = request.get_json()["channel_name"] # from JSON body
	old_channel_name = request.args["channel_name"] # from query string
	if old_channel_name is None:
		return make_response("Channel name not provided", 400)

	channel_exists = ChannelModel.query.filter_by(channel=old_channel_name).first()
	if not channel_exists:
		return make_response("Channel doesn't exist", 404)
	db.session.delete(channel_exists)

	new_channel = ChannelModel(channel=new_channel_name)
	db.session.add(new_channel)
	db.session.commit()
	return make_response("Channel name updated", 200)
