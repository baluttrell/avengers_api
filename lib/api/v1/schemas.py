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
        return avenger_models.Death(**data)


class AvengerSchema(Schema):
    id = fields.Integer()
    url = fields.String()
    name = fields.String()
    appearances = fields.Integer()
    current = fields.Boolean()
    gender = fields.String()
    probationary = fields.Date()
    full_reserve = fields.Date()
    year = fields.Integer()
    honorary = fields.String()
    notes = fields.String()

    deaths = fields.Nested(lambda: DeathSchema, exclude=["avenger"], unknown=EXCLUDE, many=True)

    @post_load
    def load_avenger(self, data, *_args, **_kwargs):
        return avenger_models.Avenger(**data)
