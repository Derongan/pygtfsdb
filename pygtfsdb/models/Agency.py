from Base import Base
from sqlalchemy import Column, String, Integer


class Agency(Base):
    __tablename__ = 'agency'

    agency_id = Column(String, default=None)
    agency_name = Column(String, nullable=False)
    agency_url = Column(String, nullable=False, unique=True)
    agency_timezone = Column(String, nullable=False)

    agency_lang = Column(String, default=None)
    agency_phone = Column(String, default=None)
    agency_fare_url = Column(String, default=None)
    agency_email = Column(String, default=None)

    pid = Column(Integer, primary_key=True)
