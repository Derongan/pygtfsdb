import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy.orm import sessionmaker
from zipfile import ZipFile
from StringIO import StringIO
import csv
from models import *


class GtfsDb(object):
    def __init__(self, url):
        """

        :param url: The url of the gtfs archive
        """
        self.url = url

    def load(self, dbstring):
        """
        Download the zipfile and extract it into objects
        :param dbstring: The string specifying the database to write to
        :return:
        """
        engine = create_engine(dbstring)
        Base.metadata.create_all(engine, checkfirst=True)

        session = sessionmaker(bind=engine)()

        response = requests.get(self.url, stream=True)

        zipped_gtfs = ZipFile(StringIO(response.content))

        with zipped_gtfs.open('agency.txt') as agency_fp:
            reader = csv.DictReader(agency_fp, delimiter=",")
            for row in reader:
                session.add(Agency(**row))

            session.commit()

        with zipped_gtfs.open('calendar.txt') as calendar_fp:
            reader = csv.DictReader(calendar_fp, delimiter=",")

            for row in reader:
                session.add()

        session.close()


if __name__ == "__main__":
    gt = GtfsDb(
        "https://api.transitfeeds.com/v1/getLatestFeedVersion?feed=vermont-translines%2F566&key=5fbcd353-bfde-4f01-b4b6-f4668a87729d")

    gt.load('sqlite:///test.db')
