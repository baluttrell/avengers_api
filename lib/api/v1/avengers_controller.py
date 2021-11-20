from lib.models import get_session, avenger_models
from lib.api.v1 import schemas

from flask import Blueprint, request

GET = "GET"
POST = "POST"


v1_avengers_bp = Blueprint("v1_avengers_bp", __name__, url_prefix="/api/v1/avengers")


@v1_avengers_bp.route("", methods=[GET, POST])
def get_all_avengers():
    """
    Return all of the avengers current in the database, based on any filters provided in query parameters or a JSON
    payload
    """
    return schemas.AvengerSchema(many=True).dumps(build_query(avenger_models.Avenger, get_session()))


@v1_avengers_bp.route("/<int:avenger_id>", methods=[GET])
def get_avenger(avenger_id):
    """
    Return all of the avengers current in the database
    """
    return schemas.AvengerSchema(many=True).dumps(avenger_models.Avenger.fetch_prototype(get_session()).get(avenger_id))


def build_query(model, session):

    filters = []

    base_query = model.fetch_prototype(session)

    parameters = request.args

    base_query.filter(*filters)

    return base_query.all()


