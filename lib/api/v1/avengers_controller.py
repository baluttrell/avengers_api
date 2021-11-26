from lib.models import get_session, avenger_models
from lib.api.v1 import schemas

from flask import Blueprint, jsonify
from marshmallow import EXCLUDE

GET = "GET"


v1_avengers_bp = Blueprint("v1_avengers_bp", __name__, url_prefix="/api/v1/avengers")


@v1_avengers_bp.route("", methods=[GET])
def get_all_avengers():
    """
    Return all of the avengers current in the database, based on any filters provided in query parameters or a JSON
    payload
    """
    return schemas.AvengerSchema(many=True, unknown=EXCLUDE) \
        .dumps(build_query(avenger_models.Avenger, get_session()))


@v1_avengers_bp.route("/<int:avenger_id>", methods=[GET])
def get_avenger(avenger_id):
    """
    Return all of the avengers current in the database
    """
    return schemas.AvengerSchema(unknown=EXCLUDE) \
        .dumps(avenger_models.Avenger.fetch_prototype(get_session()).get(avenger_id))


@v1_avengers_bp.route("/<int:avenger_id>/probability", methods=[GET])
def get_avenger_return_probability(avenger_id):
    """
    Return the probability that the avenger identified pro the provided avenger_id will return if they die again
    """
    return jsonify(avenger_models.Avenger.get_return_probability(avenger_id, get_session()))


def build_query(model, session):
    """
    Construct a query based on the model, session and request object for this request context
    :param model: The model on which to base the database query
    :param session: The database session to use
    """
    filters = []

    # TODO: Add filters based on query params and/or JSON payload in post

    base_query = model.fetch_prototype(session)

    base_query.filter(*filters)

    return base_query.all()


