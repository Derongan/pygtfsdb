from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from Base import Base
from GTFSFeed import GTFSFeed


class Stop(Base):
    __tablename__ = 'stop'

    stop_id = Column(String, nullable=False)
    stop_code = Column(String, default=None)

    stop_name = Column(String, nullable=False)
    stop_desc = Column(String, default=None)
    stop_lat = Column(Float, nullable=False)
    stop_lon = Column(Float, nullable=False)

    # TODO Implement spatial types for postgis or even sqlite

    zone_id = Column(String, default=None)
    stop_url = Column(String, default=None)
    location_type = Column(String, default=None)
    parent_station = Column(Integer, default=0)

    stop_timezone = Column(String, default=None)

    wheelchair_boarding = Column(Integer, default=0)

    pid = Column(Integer, primary_key=True, autoincrement=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id))

    gtfsfeed = relationship('GTFSFeed', back_populates='stops')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)

    @classmethod
    def add_geom(cls):
        cls.geom = Column(Geometry('POINT'))
