from lib.models import avenger_models

from marshmallow import Schema, fields, post_load, EXCLUDE


class DeathSchema(Schema):
    id = fields.Integer()
    avenger_id = fields.Integer()
    death = fields.Boolean()
    returned = fields.Boolean()
    sequence = fields.Integer()

    avenger = fields.Nested(lambda: AvengerSchema, exclude=["deaths"], unknown=EXCLUDE)

    @post_load
    def load_death(self, data, *_args, **_kwargs):
        """
        Return the data provided in the Death model
        :param data: The data to load into a Death model instance
        """
        return avenger_models.Death(**data)


class AvengerSchema(Schema):
    id = fields.Integer()
    url = fields.String()
    name = fields.String()
    appearances = fields.Integer()
    current = fields.Boolean()
    gender = fields.String()
    probationary = fields.Date(format="%y-%b")
    full_reserve = fields.Date(format="%y-%b")
    year = fields.Integer()
    years_since_joining = fields.Integer(dump_only=True)
    honorary = fields.String()
    notes = fields.String()

    deaths = fields.Nested(lambda: DeathSchema, exclude=["avenger"], unknown=EXCLUDE, many=True)

    @post_load
    def load_avenger(self, data, *_args, **_kwargs):
        """
        Return the data provided in the Avenger model
        :param data: The data to load into a Avenger model instance
        """
        return avenger_models.Avenger(**data)
