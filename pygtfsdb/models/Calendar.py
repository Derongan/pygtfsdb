from Base import Base
from sqlalchemy import Column, String, Boolean, Date, Integer


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

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    pid = Column(Integer, autoincrement=True, primary_key=True)
