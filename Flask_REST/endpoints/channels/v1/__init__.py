from flask import Blueprint
from flask_restful import MethodView

class Channels(MethodView):
	# update imports here to define version
	from Flask_REST.endpoints.channels.common.post import post 
	from Flask_REST.endpoints.channels.common.get import get
	from Flask_REST.endpoints.channels.common.put import put
	from Flask_REST.endpoints.channels.common.delete import delete

channel_view = Channels.as_view("channels")
channel_endpoint = Blueprint("channel_bp", __name__, url_prefix="/v1")
channel_endpoint.add_url_rule("/channels", view_func=channel_view)
