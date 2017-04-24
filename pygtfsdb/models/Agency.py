from Base import Base
from sqlalchemy import Column, String, Integer

class Agency(Base):
    __tablename__ = 'agency'

    agency_id = Column(String, nullable=True)
    agency_name = Column(String)
    agency_url = Column(String)
    agency_timezone = Column(String)

    agency_lang = Co