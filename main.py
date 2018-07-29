from flask import Flask, render_template
from flask_caching import Cache
import requests
import json
import controller as ctrl

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = './cache'
app.cache = Cache(app)

keys = json.loads(open('./keys/keys.json').read())

@app.route('/api/<word>')
def get_a_word(word):
    return get_word(word)

@app.route('/api/add/<group>/<word>')
def add_a_word(group, word):
    new_word = get_word(word)
    ctrl.add_word(group, word);
    return new_word;


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
