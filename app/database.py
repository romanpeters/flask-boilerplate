import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemyBase = declarative_base()
engine = sa.create_engine("sqlite:///sqlite.db", echo=False)
Session = sessionmaker(bind=engine)


class Table(SQLAlchemyBase):
    __tablename__ = 'Examples'
    example_id = sa.Column(sa.String(8), primary_key=True)


SQLAlchemyBase.metadata.create_all(engine)
