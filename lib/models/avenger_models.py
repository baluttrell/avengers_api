from lib.models import Base

from sqlalchemy.ext import hybrid
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_relationship

import datetime
import sqlalchemy as sa


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

    deaths = relationship("Death", back_populates="avenger", order_by="asc(Death.sequence)")

    @hybrid.hybrid_property
    def years_since_joining(self):
        """
        Return the number of years the Avenger has been a member by subtracting the year they joined from the current
        year
        """
        current_year = datetime.datetime.now().year

        return current_year - self.year


class Death(Base):
    __tablename__ = "deaths"

    id = sa.Column("id", sa.BigInteger, primary_key=True)
    avenger_id = sa.Column("avenger_id", sa.BigInteger, sa.ForeignKey("avengers.id"), nullable=False)

    death = sa.Column("death", sa.Boolean)
    returned = sa.Column("returned", sa.Boolean)
    sequence = sa.Column("sequence", sa.BigInteger, nullable=False)

    avenger = relationship("Avenger", back_populates="deaths", uselist=False)


class Log(Base):
    __tablename__ = "logs"

    id = sa.Column("id", sa.BigInteger, primary_key=True)
    context_id = sa.Column("context_id", sa.BigInteger)
    context_type = sa.Column("context_type", sa.Unicode(255))
    what = sa.Column("what", sa.Unicode(255), nullable=False)
    who = sa.Column("who", sa.Unicode(255), nullable=False)
    when = sa.Column("when", sa.DateTime, nullable=False)
    custom1 = sa.Column("custom1", sa.UnicodeText)
    custom2 = sa.Column("custom2", sa.UnicodeText)
    custom3 = sa.Column("custom3", sa.UnicodeText)

    context = generic_relationship(context_type, context_id)
