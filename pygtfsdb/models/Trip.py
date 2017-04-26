from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from Base import Base
from GTFSFeed import GTFSFeed
from Calendar import Calendar
from Route import Route


class Trip(Base):
    __tablename__ = 'trip'

    # TODO Flesh out. At the moment this just has the most basic capabilities

    service_id = Column(Integer, ForeignKey(Calendar.pid), nullable=False)  # Connects to calendar table actually
    calendar = relationship("Calendar")

    route_id = Column(Integer, ForeignKey(Route.pid), nullable=False)
    route = relationship("Route")

    trip_id = Column(String, nullable=False)

    pid = Column(Integer, primary_key=True, autoincrement=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id))

    gtfsfeed = relationship('GTFSFeed', back_populates='trips')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)
