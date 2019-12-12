from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word, GameWord, Game
from app.api.errors import bad_request
from flask import request, jsonify, url_for

# 制作-添加游戏单词，在图片上选中框后添加词汇
@bp.route('/game_word', methods=['POST'])
def add_game_words():
    message = {}
    # 判断数据库是否有这个单词
    data = request.get_json()
    word = data.get('word')
    if Word.query.filter_by(word=word).first() is None:
        message['word']="词库里无该单词，无法添加"
    if message:
        return bad_request(message)

    fromList = data.get('mouseFromList')
    print(fromList)
    toList = data.get('mouseToList')

    for i in range(len(fromList)):
        game_word = GameWord()
        attr = {}
        attr['word'] = word
        attr['game_img'] = data.get('game_img')
        attr['x1'] = int(fromList[i]['x'])
        attr['y1'] = int(fromList[i]['y'])
        attr['x2'] = int(toList[i]['x'])
        attr['y2'] = int(toList[i]['y'])
        game_word.set_game_word(attr)
        db.session.add(game_word)
        db.session.commit()

    response = jsonify(game_word.to_dict())
    response.status_code = 201
    return response


