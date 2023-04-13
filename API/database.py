from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_database():
    return create_engine("sqlite:///sql.db")


class DB:
    def __init__(self, conn):
        self.conn = conn

    def close(self):
        self.conn.commit()
        self.conn.close()

    def initialize_db(self):
        # Base.metadata.drop_all(self.conn) enable persistence for DB - maybe need to disable later
        Base.metadata.create_all(self.conn)
