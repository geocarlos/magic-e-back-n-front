from flask import Flask, render_template, jsonify
from flask_caching import Cache
import requests
import json
import controller as ctrl

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = './cache'
app.cache = Cache(app)

keys = json.loads(open('./keys/keys.json').read())

"""
    Get a single word from the cache or from the API
"""
@app.route('/api/word/<word>')
def get_a_word(word):
    return get_word(word)

"""
    Get words grouped according to a given letter
"""
@app.route('/api/group/<group>')
def get_group_of_words(group):
    words = ctrl.get_words_by_group(group)
    return jsonify(words)

"""
    Get all groups and words
"""
@app.route('/api/words')
def get_all_words():
    words = ctrl.get_all_word_groups()
    return jsonify(words)

"""
    Add a word to a group according to a given letter
"""
@app.route('/api/add/<group>/<word>')
def add_a_word(group, word):
    new_word = json.loads(get_word(word))
    ctrl.add_word(group, new_word['results'][0])
    return jsonify(new_word)

"""
    Get and cache a word from the API
"""
def get_word(word):
    cached = app.cache.get(word)
    if(cached):
        return cached

    app_id = keys['app_id']
    app_key = keys['app_key']

    language = 'en'

    # url = 'https://od-api.oxforddictionaries.com:443/api/v1/wordlist/' + language + '/registers=Rare;domains=Art'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word

    r = None

    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        app.cache.set(word, r.text)
    except:
        return '{"error": "Unable to fetch word"}'

    return r.text

if __name__ == '__main__':
    app.secret_key = 'geowildcat_magic_ee'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
