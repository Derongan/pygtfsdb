from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Base import Base


class GTFSFeed(Base):
    __tablename__ = 'gtfsfeed'

    gtfsfeed_id = Column(Integer, autoincrement=True, primary_key=True)

    gtfs_name = Column(String, unique=True)

    agencies = relationship('Agency', back_populates='gtfsfeed')

    calendars = relationship('Calendar', back_populates='gtfsfeed')