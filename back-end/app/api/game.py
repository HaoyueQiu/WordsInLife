from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word, GameWord, Game
from flask import request


@bp.route('/game', methods=['POST'])
def add_game():
    data = request.get_json()
    """
    if(data.get('img_name') in GameWord.query.all().)):
     """


@bp.route('/game', methods=['GET'])
def get_words():
    a = Game.query.all()
    words = []
    for i in range(len(a)):
        words.append({'EN': a[i].img_name, 'word_subject': a[i].word_subject})
    return jsonify(words)
