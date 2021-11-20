from dotenv import load_dotenv
from yaml import safe_load

import os

ENV_KEY = "ENV"
DATABASE_PASSWORD_KEY = "DATABASE_PASSWORD"
DATABASE_USER_KEY = "DATABASE_USER"
DATABASE_URL_KEY = "database_url"
DATABASE_PASSWORD_VARIABLE_KEY = "<db_password>"
DATABASE_USER_VARIABLE_KEY = "<db_user>"

load_dotenv()

ENV = os.getenv(ENV_KEY)
DATABASE_PASSWORD = os.getenv(DATABASE_PASSWORD_KEY)
DATABASE_USER = os.getenv(DATABASE_USER_KEY)

config = safe_load(open("config.yaml")).get(ENV, {})


def database_url():
    """
    Return the database URL to use when initializing the application for migrations or runtime. The database username
    and password are interpolated if required by the URL (denoted by the DATABASE_USER_VARIABLE_KEY and
    DATABASE_PASSWORD_VARIABLE_KEY), and the values exist in the respective environment variables. If the username
    and/or password are required by the URL, but not present in the environment variables, an exception is raised.
    """
    if DATABASE_USER_VARIABLE_KEY in config.get(DATABASE_URL_KEY) and not DATABASE_USER:
        raise BootstrapException(f"Expected database user in environment variable {DATABASE_USER_KEY},"
                                 " but none was provided")

    if DATABASE_PASSWORD_VARIABLE_KEY in config.get(DATABASE_URL_KEY) and not DATABASE_PASSWORD:
        raise BootstrapException(f"Expected database password in environment variable {DATABASE_PASSWORD_KEY},"
                                 " but none was provided")

    return config.get(DATABASE_URL_KEY) \
        .replace(DATABASE_PASSWORD_VARIABLE_KEY, DATABASE_PASSWORD) \
        .replace(DATABASE_USER_VARIABLE_KEY, DATABASE_USER)


class BootstrapException(Exception):
    pass
