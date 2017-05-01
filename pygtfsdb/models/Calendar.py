from sqlalchemy.orm import relationship

from Base import Base
from Agency import Agency
from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey

from GTFSFeed import GTFSFeed


class Calendar(Base):
    __tablename__ = 'calendar'

    service_id = Column(String, nullable=False)

    monday = Column(Boolean, nullable=False, default=False)
    tuesday = Column(Boolean, nullable=False, default=False)
    wednesday = Column(Boolean, nullable=False, default=False)
    thursday = Column(Boolean, nullable=False, default=False)
    friday = Column(Boolean, nullable=False, default=False)
    saturday = Column(Boolean, nullable=False, default=False)
    sunday = Column(Boolean, nullable=False, default=False)


    # TODO Figure out how to handle these. They should be set but sometimes are not
    start_date = Column(Date)
    end_date = Column(Date)

    pid = Column(Integer, autoincrement=True, primary_key=True)

    gtfsfeed_id = Column(Integer, ForeignKey(GTFSFeed.gtfsfeed_id))

    gtfsfeed = relationship('GTFSFeed', back_populates='calendars')


    def __init__(self, **kwargs):
        """Ignore extra columns"""
        self.__dict__.update(kwargs)
