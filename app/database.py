import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemyBase = declarative_base()
engine = sa.create_engine("sqlite:///sqlite.db", echo=False)
Session = sessionmaker(bind=engine)


class Reservations(SQLAlchemyBase):
    __tablename__ = 'Reservations'
    reservation_id = sa.Column(sa.String(), primary_key=True)
    ts_id = sa.Column(sa.String())
    user_id = sa.Column(sa.Integer())

class Users(SQLAlchemyBase):
    __tablename__ = 'Users'
    user_id = sa.Column(sa.Integer(), primary_key=True)
    password = sa.Column(sa.String())
    first_name = sa.Column(sa.String())
    last_name = sa.Column(sa.String())
    cookies = sa.Column(sa.String())

class TimeSlots(SQLAlchemyBase):
    __tablename__ = 'TimeSlots'
    ts_id = sa.Column(sa.String(), primary_key=True)
    title = sa.Column(sa.String())
    start_time = sa.Column(sa.DateTime)
    end_time = sa.Column(sa.DateTime)


SQLAlchemyBase.metadata.create_all(engine)
