from lib.models import Base

from sqlalchemy.ext import hybrid
from sqlalchemy.orm import relationship, selectinload, joinedload
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

    @classmethod
    def fetch_prototype(cls, session):
        """
        Return the query prototype for the Avenger class. The prototype can be modified further by the caller
        :param session: The database session to use
        """
        return session \
            .query(cls) \
            .options(selectinload(cls.deaths))

    @classmethod
    def get_return_probability(cls, avenger_id, session):
        """
        Return the percent probability that the avenger identified by the provided avenger_id will return from death.
        If the avenger has already returned from their most recent death, the calculation will assume the avenger dies
        again, before calculating the return chance
        :param avenger_id: The unique identifier of the avenger to calculate the percent chance of return
        :param session: The database session to use
        """
        avenger = cls.fetch_prototype(session).get(avenger_id)  # Fetch the avenger

        # Calculate the number of deaths to base the calculation off of.
        deaths = len(avenger.deaths) if not avenger.deaths[-1].returned else len(avenger.deaths) + 1

        # Fetch the count of avengers with the same number of deaths, and their number of returns
        matching_avengers = session \
            .query(cls.id,
                   sa.func.count(Death.id),
                   sa.func.sum(sa.case(
                       (Death.returned == True, 1),
                       else_=0))) \
            .join(cls.deaths) \
            .having(sa.func.count(Death.id) == deaths) \
            .group_by(cls.id) \
            .all()

        # Calculate the total number of returns in the fetched list
        total_returns = sum([item[2] for item in matching_avengers])

        # Calculate the return probability by dividing the total returns by the number of avengers and the number of
        # deaths
        return (total_returns / len(matching_avengers) / deaths)


class Death(Base):
    __tablename__ = "deaths"

    id = sa.Column("id", sa.BigInteger, primary_key=True)
    avenger_id = sa.Column("avenger_id", sa.BigInteger, sa.ForeignKey("avengers.id"), nullable=False)

    death = sa.Column("death", sa.Boolean)
    returned = sa.Column("returned", sa.Boolean)
    sequence = sa.Column("sequence", sa.BigInteger, nullable=False)

    avenger = relationship("Avenger", back_populates="deaths", uselist=False)

    @classmethod
    def fetch_prototype(cls, session):
        """
        Return the query prototype for the Death class. The prototype can be modified further by the caller
        :param session: The database session to use
        """
        return session \
            .query(cls) \
            .options(joinedload(cls.avenger))


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
