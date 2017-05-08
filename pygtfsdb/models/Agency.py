from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Base import Base
from GTFSFeed import GTFSFeed


class Agency(Base):
    __tablename__ = 'agency'

    agency_id = Column(String, default=None, index=True)
    agency_name = Column(String, nullable=False)
    agency_url = Column(String, nullable=False)
    agency_timezone = Column(String, nullable=False)

    agency_lang = Column(String, default=None)
    agency_phone = Column(String, default=None)
    agency_fare_url = Column(String, default=None)
    agency_email = Column(String, default=None)

    pid = Column(Integer, primary_key=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id), index=True)

    gtfsfeed = relationship('GTFSFeed', back_populates='agencies')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)
