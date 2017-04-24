from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    def __init__(self):
        pass


Base = declarative_base(cls=Base)
