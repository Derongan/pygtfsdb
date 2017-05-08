import csv
from StringIO import StringIO
from datetime import datetime
from zipfile import ZipFile

import requests
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, update, insert

from models import *

import logging

logging.basicConfig(level=logging.INFO)


class GtfsDb(object):
    @classmethod
    def empty_string_to_none(cls, dict):
        for k, v in dict.items():
            if v is "":
                dict[k] = None

        return dict

    def __init__(self, dbstring, spatial=False, batch_size=100):
        """

        :param dbstring: The string sqlalchemy will use to connect
        :param spatial: Does the database support spatial datatypes?
        """
        self.dbstring = dbstring

        self.spatial = spatial
        self.batch_size = batch_size

        self.engine = create_engine(self.dbstring)

        if self.spatial:
            Stop.add_geom()

        Base.metadata.create_all(self.engine, checkfirst=True)

    def load(self, url, gtfs_name):
        """
        Download the zipfile and extract it into objects
        :param url: The string specifying gtfs archive url. If it is a file object we use that instead
        :param gtfs_name: The name of the current gtfs org
        :return:
        """

        session = sessionmaker(bind=self.engine)()

        if type(url) == ZipFile:
            zipped_gtfs = url
        else:
            response = requests.get(url, stream=True)

            zipped_gtfs = ZipFile(StringIO(response.content))

        try:
            feed_row = GTFSFeed(gtfs_name=gtfs_name)
            session.add(feed_row)
            i = 0
            logging.info("Loading agencies")
            with zipped_gtfs.open('agency.txt') as agency_fp:
                reader = csv.DictReader(agency_fp, delimiter=",")
                for row in reader:
                    row = GtfsDb.empty_string_to_none(row)
                    a = Agency(**row)
                    feed_row.agencies.append(a)
                    session.add(a)

                    i += 1

                    if i % self.batch_size == 0:
                        session.commit()
                session.commit()

            logging.info("Loading calendars")
            with zipped_gtfs.open('calendar.txt') as calendar_fp:
                reader = csv.DictReader(calendar_fp, delimiter=",")
                i = 0
                for row in reader:
                    row = GtfsDb.empty_string_to_none(row)

                    try:
                        row['start_date'] = datetime.strptime(row['start_date'], '%Y%m%d')
                    except (ValueError, TypeError):
                        row['start_date'] = None
                    try:
                        row['end_date'] = datetime.strptime(row['end_date'], '%Y%m%d')
                    except (ValueError, TypeError):
                        row['end_date'] = None

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

                    i += 1

                    if i % self.batch_size == 0:
                        session.commit()

                session.commit()

            logging.info("Loading routes")
            with zipped_gtfs.open('routes.txt') as route_fp:
                reader = csv.DictReader(route_fp, delimiter=",")
                i = 0
                for row in reader:
                    row = GtfsDb.empty_string_to_none(row)

                    r = Route(**row)
                    feed_row.routes.append(r)
                    session.add(r)

                    i += 1

                    if i % self.batch_size == 0:
                        session.commit()

                session.commit()

            logging.info("Loading stops")
            with zipped_gtfs.open('stops.txt') as stop_fp:
                reader = csv.DictReader(stop_fp, delimiter=",")
                i = 0
                for row in reader:
                    row['geom'] = "POINT({0} {1})".format(row['stop_lon'], row['stop_lat'])
                    row = GtfsDb.empty_string_to_none(row)

                    s = Stop(**row)
                    feed_row.stops.append(s)
                    session.add(s)

                    i += 1

                    if i % self.batch_size == 0:
                        session.commit()

                session.commit()

            logging.info("Loading trips")
            with zipped_gtfs.open('trips.txt') as trip_fp:
                reader = csv.DictReader(trip_fp, delimiter=",")
                i = 0
                objects = []
                for row in reader:
                    row = GtfsDb.empty_string_to_none(row)

                    t = Trip(**row)
                    t.gtfsfeed_id = feed_row.gtfsfeed_id

                    objects.append(t);

                    i += 1

                    if i % self.batch_size == 0:
                        session.bulk_save_objects(objects)

                        objects = []

                session.bulk_save_objects(objects)
                del objects

                session.commit()

                temp_route = Table("tt", Base.metadata, Column('pid', Integer, primary_key=True),
                                  Column('route_pid', Integer),
                                  prefixes=['TEMPORARY'])
                temp_route.create(bind=self.engine)
                route_sel = select([Trip.pid, Route.pid]).where(Trip.route_id == Route.route_id).where(
                    Trip.gtfsfeed == feed_row).where(Route.gtfsfeed == feed_row)

                session.execute(temp_route.insert().from_select(['pid', 'route_pid'], route_sel))

                session.execute(Trip.__table__.update().values(route_pid=temp_route.c.route_pid).where(
                    temp_route.c.pid == Trip.pid))

                session.commit()

                temp_route.drop(bind=self.engine)
                Base.metadata.remove(temp_route)
                
                
                temp_calendar = Table("tt", Base.metadata, Column('pid', Integer, primary_key=True),
                                  Column('service_pid', Integer),
                                  prefixes=['TEMPORARY'])
                temp_calendar.create(bind=self.engine)
                calendar_sel = select([Trip.pid, Calendar.pid]).where(Trip.service_id == Calendar.service_id).where(
                    Trip.gtfsfeed == feed_row).where(Calendar.gtfsfeed == feed_row)

                session.execute(temp_calendar.insert().from_select(['pid', 'service_pid'], calendar_sel))

                session.execute(Trip.__table__.update().values(service_pid=temp_calendar.c.service_pid).where(
                    temp_calendar.c.pid == Trip.pid))

                session.commit()

                temp_calendar.drop(bind=self.engine)
                Base.metadata.remove(temp_calendar)

                # route_sel = select([Route.pid]).where(Trip.route_id == Route.route_id).where(
                #     Trip.gtfsfeed == feed_row).where(Route.gtfsfeed == feed_row)
                # calendar_sel = select([Calendar.pid]).where(Trip.service_id == Calendar.service_id).where(
                #     Trip.gtfsfeed == feed_row).where(Calendar.gtfsfeed == feed_row)
                #
                # session.execute(Trip.__table__.update().values(route_pid=route_sel, service_pid=calendar_sel).where(
                #     StopTime.gtfsfeed == feed_row))

                session.commit()

            logging.info("Loading stop times")
            with zipped_gtfs.open('stop_times.txt') as time_fp:
                reader = csv.DictReader(time_fp, delimiter=",")
                i = 0

                objects = []

                for row in reader:
                    row = GtfsDb.empty_string_to_none(row)

                    # TODO handle times above 24hr (ie next day on route)
                    try:
                        row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M:%S').time()
                    except (ValueError, TypeError):
                        row['arrival_time'] = None
                    try:
                        row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M:%S').time()
                    except (ValueError, TypeError):
                        row['departure_time'] = None

                    t = StopTime(**row)
                    t.gtfsfeed_id = feed_row.gtfsfeed_id

                    objects.append(t)
                    # t.trip = session.query(Trip).filter(Trip.trip_id == t.trip_id).filter(
                    #     Trip.gtfsfeed == feed_row).first()
                    # t.stop = session.query(Stop).filter(Stop.stop_id == t.stop_id).filter(
                    #     Stop.gtfsfeed == feed_row).first()



                    # feed_row.stop_times.append(t)
                    # session.add(t)
                    #
                    i += 1

                    if i % self.batch_size == 0:
                        session.bulk_save_objects(objects)

                        logging.info("Finished {0}".format(i))

                        objects = []

                session.bulk_save_objects(objects)
                del objects[:]
                del objects

                session.commit()

                temp_trip = Table("tt", Base.metadata, Column('pid', Integer, primary_key=True),
                                  Column('trip_pid', Integer),
                                  prefixes=['TEMPORARY'])
                temp_trip.create(bind=self.engine)
                trip_sel = select([StopTime.pid, Trip.pid]).where(StopTime.trip_id == Trip.trip_id).where(
                    Trip.gtfsfeed == feed_row).where(StopTime.gtfsfeed == feed_row)

                session.execute(temp_trip.insert().from_select(['pid', 'trip_pid'], trip_sel))

                session.execute(StopTime.__table__.update().values(trip_pid=temp_trip.c.trip_pid).where(
                    temp_trip.c.pid == StopTime.pid))

                session.commit()

                temp_trip.drop(bind=self.engine)
                Base.metadata.remove(temp_trip)

                temp_stop = Table("tt", Base.metadata, Column('pid', Integer, primary_key=True),
                                  Column('stop_pid', Integer),
                                  prefixes=['TEMPORARY'])

                temp_stop.create(bind=self.engine)
                stop_sel = select([StopTime.pid, Stop.pid]).where(StopTime.stop_id == Stop.stop_id).where(
                    Stop.gtfsfeed == feed_row).where(StopTime.gtfsfeed == feed_row)

                session.execute(temp_stop.insert().from_select(['pid', 'stop_pid'], stop_sel))

                session.execute(StopTime.__table__.update().values(stop_pid=temp_stop.c.stop_pid).where(
                    temp_stop.c.pid == StopTime.pid))

                session.commit()
                temp_trip.drop(bind=self.engine)
                Base.metadata.remove(temp_stop)

        except:
            raise
        finally:
            zipped_gtfs.close()
            session.close()


if __name__ == "__main__":
    gt = GtfsDb('postgresql://postgres:@localhost:5432/alexabus', spatial=True, batch_size=3000)

    zf = ZipFile("test_data/unitransgtfs.zip")
    gt.load(zf, "Test")
