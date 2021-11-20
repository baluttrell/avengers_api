from lib import database_url

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()
Session = None


def get_session():
    """
    Return a scoped database session using the configured database URL. If no session has been created during this
    runtime, a new engine and session factory are instantiated before returning a new scoped session.
    """
    global Session

    if not Session:
        engine = create_engine(database_url())
        Session = scoped_session(sessionmaker(bind=engine))

    return Session()


@contextmanager
def session_scope():
    """
    Yield a new session for use within a context ('with' block). If a SQLalchemy exception is raised within the block,
    the session will be automatically rolled back
    """
    session = get_session()

    try:
        yield session

    except SQLAlchemyError:
        session.rollback()
