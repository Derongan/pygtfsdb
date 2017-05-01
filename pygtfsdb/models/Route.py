from sqlalchemy import CheckConstraint
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Base import Base
from GTFSFeed import GTFSFeed


class Route(Base):
    __tablename__ = 'route'

    __table_args__ = (
        CheckConstraint('NOT(route_short_name IS NULL AND route_long_name IS NULL)'),
    )

    route_id = Column(String, nullable=False)
    agency_id = Column(String, default=None)

    route_short_name = Column(String)
    route_long_name = Column(String)

    route_desc = Column(String, default=None)

    route_type = Column(Integer, nullable=False)

    route_url = Column(String, default=None)
    route_color = Column(String, default=None)
    route_text_color = Column(String, default=None)

    pid = Column(Integer, primary_key=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id))

    gtfsfeed = relationship('GTFSFeed', back_populates='routes')

    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)
