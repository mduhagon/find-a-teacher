# Api Blueprint. This Blueprint will hold all routes
# that return JSON data instead of HTML

from flask import Blueprint
from teachersapp.models import TeachingProfile
from flask import jsonify, request

api = Blueprint('api', __name__)


@api.route("/api/get_profiles_in_radius")
def get_profiles_in_radius():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lng'))
    radius = int(request.args.get('radius'))

    # TODO: Validate the input!

    profiles = TeachingProfile.get_profiles_within_radius(lat=latitude, lng=longitude, radius=radius)
    result = []
    for p in profiles:
        result.append(p.toDict())
    return jsonify(result)