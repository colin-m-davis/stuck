from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Note(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)
    w = Column(Integer, nullable=False, default=360)
    h = Column(Integer, nullable=False, default=360)


engine = create_engine('sqlite:///notes.db')
if not inspect(engine).has_table('note'):
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
