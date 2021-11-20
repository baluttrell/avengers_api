from alembic.config import Config
from alembic import command

import csv
import collections
import requests


VERSION_KEY = "<version>"
AVENGER_DATA_VERSION = "9b532414ecc7d7efdf9f0f4435f4f19de7e6f73a"
AVENGER_DATA_URL = rf"https://raw.githubusercontent.com/fivethirtyeight/data/{VERSION_KEY}/avengers/avengers.csv"

# The namedtuple used to store instances of Avenger data from the static repository. Note that the order of the
# arguments matches the order of the columns in the CSV file.
AvengerData = collections.namedtuple("AvengerData", ["url",
                                                     "name",
                                                     "appearances",
                                                     "current",
                                                     "gender",
                                                     "probationary",
                                                     "full_reserve",
                                                     "year",
                                                     "years_since_joining",
                                                     "honorary",
                                                     "death1",
                                                     "return1",
                                                     "death2",
                                                     "return2",
                                                     "death3",
                                                     "return3",
                                                     "death4",
                                                     "return4",
                                                     "death5",
                                                     "return5",
                                                     "notes"])


def run_migrations():
    """
    Execute all alembic migrations, starting with the current revision as tracked in the configured database
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def fetch_avenger_data():
    """
    Fetch the configured static version of the avenger data from the configured git URL
    """
    response = requests.get(AVENGER_DATA_URL.replace(VERSION_KEY, AVENGER_DATA_VERSION))

    if response:
        reader = csv.reader(response.text.splitlines())

        _header = next(reader, None)  # Iterate over the header

        return [AvengerData(*item) for item in reader]

    else:
        return ""


if __name__ == "__main__":
    run_migrations()
