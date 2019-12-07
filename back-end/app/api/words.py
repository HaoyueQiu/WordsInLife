from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word


@bp.route('/wordSubject', methods=['GET'])
def get_words_subject():
    a = WordSubject.query.order_by(WordSubject.wordsubject).all()
    subject = []
    for i in range(len(a)):
        subject.append(a[i].wordsubject)

    '''
    subject = ['body', 'classroom', 'food', 'job', 'kitchen', 'plant', 'vehicles', 'stationery']
    for i in range(8):
        w = WordSubject()
        w.wordsubject = subject[i]
        db.session.add(w)
        db.session.commit()
    '''
    return jsonify(subject)


@bp.route('/words', methods=['GET'])
#def get_word(wordSubject):
def get_word():
    # 后续改成类别！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！11
    a = Word.query.all()
    words = []
    for i in range(len(a)):
        words.append({'EN': a[i].word, 'CN': a[i].meaning})
    return jsonify(words)