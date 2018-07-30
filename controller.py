from model import Group, Entry, WordGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
    Connect to our SQLite database and return a Session object
"""
engine = create_engine("sqlite:///db/app.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def add_word(group, w_data):
    print(w_data['lexicalEntries'][0]['pronunciations'][0]['audioFile'])
    group_letter = group
    word = w_data['word']
    audio = w_data['lexicalEntries'][0]['pronunciations'][0]['audioFile']
    ipa_spelling = w_data['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
    group = None
    try:
        group = session.query(Group).filter_by(letter=group_letter).one()
    except Exception:
        print('Go on and add new Group')
    if not group:
        group = Group(letter=group_letter)
        session.add(group)
        session.flush()
    session.add(Entry(word=word, audio=audio,
                      ipa_spelling=ipa_spelling, group_id=group.id))
    session.commit()
    session.close()


def get_all_word_groups():
    words = {}
    groups = session.query(Group).all()
    entries = session.query(Entry).all()
    for group in groups:
        words[group.letter] = {"words": []}
        for e in entries:
            words[group.letter]["words"].append({
                'word': e.word, 'audio': e.audio, 'ipa_spelling': e.ipa_spelling})

    session.close()

    return words


def get_words_by_group(group_letter):
    group = None
    word_group = {}
    word_group[group_letter] = {'words': []}
    try:
        group = session.query(Group).filter_by(letter=group_letter).one()
    except Exception:
        return {"error": "No group of words for %s" % group_letter}
    entries = session.query(Entry).filter_by(group_id=group.id)

    for e in entries:
        word_group[group_letter]['words'].append({
            'word': e.word, 'audio': e.audio, 'ipa_spelling': e.ipa_spelling})

    session.close()

    return word_group
