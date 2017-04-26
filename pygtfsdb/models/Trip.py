from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from Base import Base
from GTFSFeed import GTFSFeed
from Calendar import Calendar
from Route import Route


class Trip(Base):
    __tablename__ = 'trip'

    # TODO Flesh out. At the moment this just has the most basic capabilities
    # TODO Maybe somehow make foreign keys required

    service_pid = Column(Integer, ForeignKey(Calendar.pid))  # Connects to calendar table actually
    service_id = Column(String, nullable=False)  # Connects to calendar table actually
    calendar = relationship("Calendar")

    route_pid = Column(Integer, ForeignKey(Route.pid))
    route_id = Column(String, nullable=False)
    route = relationship("Route")

    trip_id = Column(String, nullable=False)

    pid = Column(Integer, primary_key=True, autoincrement=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id))

    gtfsfeed = relationship('GTFSFeed', back_populates='trips')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)
