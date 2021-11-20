"""load static data

Revision ID: 3eab22c80ef7
Revises: d015d71240f2
Create Date: 2021-11-20 10:32:05.379922

"""
from setup import fetch_avenger_data

from alembic import op
from sqlalchemy import orm

import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eab22c80ef7'
down_revision = 'd015d71240f2'
branch_labels = None
depends_on = None

Base = orm.declarative_base()


# These models are duplicated in the migration, since the migration represents a specific point in the lifecycle of the
# database schema. Since this load operation takes place at a known point in the schema, the model must match the schema
# as it exists at this point in the lifecycle, allowing the application's actual models to drift as requirements change
# and new features are added
class Avenger(Base):
    __tablename__ = "avengers"

    id = sa.Column("id", sa.BigInteger, primary_key=True)

    url = sa.Column("url", sa.Unicode(255))
    name = sa.Column("name", sa.Unicode(255))
    appearances = sa.Column("appearances", sa.BigInteger, nullable=False)
    current = sa.Column("current", sa.Boolean, nullable=False)
    gender = sa.Column("gender", sa.Unicode(50))
    probationary = sa.Column("probationary", sa.Date)
    full_reserve = sa.Column("full_reserve", sa.Date)
    year = sa.Column("year", sa.BigInteger)
    honorary = sa.Column("honorary", sa.Unicode(50))
    notes = sa.Column("notes", sa.UnicodeText)

    deaths = orm.relationship("Death", back_populates="avenger", order_by="asc(Death.sequence)")


class Death(Base):
    __tablename__ = "deaths"

    id = sa.Column("id", sa.BigInteger, primary_key=True)
    avenger_id = sa.Column("avenger_id", sa.BigInteger, sa.ForeignKey("avengers.id"), nullable=False)

    death = sa.Column("death", sa.Boolean)
    returned = sa.Column("returned", sa.Boolean)
    sequence = sa.Column("sequence", sa.BigInteger, nullable=False)

    avenger = orm.relationship("Avenger", back_populates="deaths", uselist=False)


def upgrade():
    """
    Load the initial schema tables with the data retrieved from the avengers git repository. This is treated as a
    migration, since the data is expected to be static, and should only be loaded once
    """
    avenger_models = load_avenger_models()

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add_all(avenger_models)
    session.commit()


def downgrade():
    """
    The data will not be removed, since there is no way to deterministically target only the initial data set, since it
    may have been mutated
    """
    pass


def load_avenger_models():
    """
    Load each instance of data from the repository into its associated model at this point in the schema lifecycle
    """
    avengers = []

    for item in fetch_avenger_data():
        # Explicitly assign each attribute of the model, so various attributes can be ignored
        avenger = Avenger(url=item.url,
                          name=item.name,
                          appearances=item.appearances,
                          current=item.current == "YES",
                          gender=item.gender,
                          probationary=parse_date(item.probationary),
                          full_reserve=parse_date(item.full_reserve),
                          year=item.year,
                          honorary=item.honorary,
                          notes=item.notes)

        for occurrence in range(1, 6):  # Iterate over the known indices of deaths (max in data range is 5)
            # If the death attribute exists and has a value, create a new Death instance and load the associated
            # instance data before adding it to the the list of deaths on the current avenger
            if getattr(item, f"death{occurrence}", None):
                avenger.deaths.append(
                    Death(death=getattr(item, f"death{occurrence}") == "YES",  # Convert string to boolean
                          returned=getattr(item, f"return{occurrence}") == "YES",  # Convert string to boolean
                          sequence=occurrence)  # Add the sequence of this death, order is important!
                )
            else:
                break  # If this is the last death, there is no reason to check subsequent iterations

        avengers.append(avenger)  # Add this avenger to the list of avengers

    return avengers


def parse_date(date_string):
    """
    Return the datetime object the provided string represents. The data is expected to be in the format of mmm-yy, but
    formatting issues in the CSV file mistakenly converted some data points to d-mmm. This function attempts to rectify
    the mistaken formatting by parsing using the first method, before attempting the second, zfilling the mistaken day
    digit to two characters, so the datetime parse completes successfully
    :param date_string: The string which to convert to a datetime object
    """
    date_obj = None

    if date_string:
        try:
            date_obj = datetime.datetime.strptime(date_string, "%b-%y")

        except ValueError:
            parts = date_string.split('-')
            parts[0] = parts[0].zfill(2)

            date_obj = datetime.datetime.strptime('-'.join(parts), "%y-%b")

    return date_obj
