from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word,UserWord
from flask import request

@bp.route('/wordSubject', methods=['GET'])
def get_words_subject():
    a = WordSubject.query.order_by(WordSubject.wordsubject).all()
    subject = []
    for i in range(len(a)):
        subject.append(a[i].wordsubject)
    return jsonify(subject)

# 传入用户的username和单词类别word_subject，从而获取该用户哪些单词还没有背诵的消息
# 对于每个类别，返回已经背诵的个数
@bp.route('/words', methods=['GET'])
def get_word():

    username = request.args.get('username')
    wordsubject = request.args.get('wordsubject')
    a = Word.query.filter_by(word_subject=wordsubject).all()
    words = []
    for i in range(len(a)):
        queryB = UserWord.query.filter_by(user=username,word=a[i].word).all()

        if len(queryB) == 0 or queryB[0].proficiency<1:
            if(len(queryB)==0):
                user_word = UserWord()
                attr = {}
                attr['user'] = username
                attr['word'] = a[i].word
                attr['proficiency'] = 0
                attr['times'] = 0
                user_word.set_attr(attr)
                db.session.add(user_word)
                db.session.commit()
            queryB = UserWord.query.filter_by(user=username, word=a[i].word).all()
            words.append({'EN': a[i].word, 'CN': a[i].meaning,'proficiency':queryB[0].proficiency,'times':queryB[0].times})
    return jsonify(words)


@bp.route('/words', methods=['POST'])
def save_word_proficiency():
    data = request.get_json()
    # save data in sql
