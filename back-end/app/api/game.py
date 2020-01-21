from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word, GameWord, Game
from flask import request
import random

@bp.route('/game', methods=['POST'])
def add_game():
    data = request.get_json()
    """
    if(data.get('img_name') in GameWord.query.all().)):
     """


# 获取游戏图的名字和类别
@bp.route('/game', methods=['GET'])
def get_game_pic():
    a = Game.query.all()
    words = []
    for i in range(len(a)):
        words.append({'EN': a[i].img_name, 'word_subject': a[i].word_subject})

    return jsonify(words)

