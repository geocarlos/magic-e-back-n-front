from model import Group, Entry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
    Connect to our SQLite database and return a Session object
"""
engine = create_engine("sqlite:///db/app.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def add_word(group_letter, word):
    group = None
    try:
        group = session.query(Group).filter_by(letter=group_letter).one()
    except Exception:
        print('Go on and add new Group')
    if not group:
        group = Group(letter=group_letter)
        session.add(group)
        session.flush()
    session.add(Entry(word=word, group_id=group.id))
    session.commit()
    session.close()

def get_words_by_group(group_letter):
    group = None
    try:
        group = session.query(Group).filter_by(letter=group_letter).one()
    except Exception:
        return {"error": "No group of words for %s"%group_letter}
    entries = session.query(Entry).filter_by(group_id=group.id)
    return entries
