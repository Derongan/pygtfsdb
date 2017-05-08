from sqlalchemy import Column, String, Integer, ForeignKey, Float, Time
from sqlalchemy.orm import relationship

from Base import Base
from GTFSFeed import GTFSFeed
from Trip import Trip
from Stop import Stop


class StopTime(Base):
    __tablename__ = 'stop_time'

    # TODO Flesh out fully, still a skeleton
    # TODO Maybe somehow make foreign keys required

    trip_pid = Column(Integer, ForeignKey(Trip.pid))
    trip_id = Column(String, nullable=False, index=True)
    trip = relationship("Trip")

    stop_pid = Column(Integer, ForeignKey(Stop.pid))
    stop_id = Column(String, nullable=False, index=True)
    stop = relationship("Stop")

    # TODO These times should be not null and should be interpolated if the value is missing.
    arrival_time = Column(Time, default=None)
    departure_time = Column(Time, default=None)

    stop_sequence = Column(Integer, nullable=False)

    timepoint = Column(Integer, default=1)

    pid = Column(Integer, primary_key=True, autoincrement=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id), index=True)

    gtfsfeed = relationship('GTFSFeed', back_populates='stop_times')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)


# class RawStopTime(Base):
#     __tablename__ = 'stop_time_raw'
#
#     trip_id = Column(String)
#
#     stop_id = Column(String)
#
#     def __init__(self, **kwargs):
#         """Ignore extra columns"""
#         self.__dict__.update(kwargs)