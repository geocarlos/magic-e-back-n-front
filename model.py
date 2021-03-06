from sqlalchemy import Table, Column, create_engine
from sqlalchemy import ForeignKey, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///db/app.db", echo=True)
Base = declarative_base(engine)

class WordGroup(object):
    def __init__(self, group, words):
        self.group = group
        self.words = words

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    letter = Column(String(80), nullable=False)


class Entry(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    word = Column(String(80), nullable=False)
    audio = Column(String(80))
    ipa_spelling = Column(String(80))
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(Group)

Base.metadata.create_all(engine)
