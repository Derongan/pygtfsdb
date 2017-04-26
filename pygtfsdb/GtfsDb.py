import csv
from StringIO import StringIO
from datetime import datetime
from zipfile import ZipFile

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *


class GtfsDb(object):
    def __init__(self, dbstring):
        """

        :param dbstring: The string sqlalchemy will use to connect
        """
        self.dbstring = dbstring

    def load(self, url, gtfs_name):
        """
        Download the zipfile and extract it into objects
        :param url: The string specifying gtfs archive url
        :param gtfs_name: The name of the current gtfs org
        :return:
        """
        engine = create_engine(self.dbstring)
        Base.metadata.create_all(engine, checkfirst=True)

        session = sessionmaker(bind=engine)()

        response = requests.get(url, stream=True)

        zipped_gtfs = ZipFile(StringIO(response.content))

        feed_row = GTFSFeed(gtfs_name=gtfs_name)
        session.add(feed_row)

        with zipped_gtfs.open('agency.txt') as agency_fp:
            reader = csv.DictReader(agency_fp, delimiter=",")
            for row in reader:
                a = Agency(**row)
                feed_row.agencies.append(a)
                session.add(a)

            session.commit()

        with zipped_gtfs.open('calendar.txt') as calendar_fp:
            reader = csv.DictReader(calendar_fp, delimiter=",")

            for row in reader:
                row['start_date'] = datetime.strptime(row['start_date'], '%Y%m%d')
                row['end_date'] = datetime.strptime(row['end_date'], '%Y%m%d')

                # Handle sqlalchemy improper conversion to boolean for sqlite (Could be a local issue)
                row['monday'] = row['monday'] == "1"
                row['tuesday'] = row['tuesday'] == "1"
                row['wednesday'] = row['wednesday'] == "1"
                row['thursday'] = row['thursday'] == "1"
                row['friday'] = row['friday'] == "1"
                row['saturday'] = row['saturday'] == "1"
                row['sunday'] = row['sunday'] == "1"


                c = Calendar(**row)
                feed_row.calendars.append(c)
                session.add(c)

            session.commit()

        with zipped_gtfs.open('routes.txt') as route_fp:
            reader = csv.DictReader(route_fp, delimiter=",")

            for row in reader:
                r = Route(**row)
                feed_row.routes.append(r)
                session.add(r)

            session.commit()

        session.close()


if __name__ == "__main__":
    gt = GtfsDb('sqlite:///test.db')

    gt.load(
        "http://transitfeeds.com/link?u=http://iportal.sacrt.com/GTFS/Unitrans/google_transit.zip", "Unitrans")
