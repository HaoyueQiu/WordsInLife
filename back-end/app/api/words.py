from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject


@bp.route('/words', methods=['GET'])
def get_words_subject():

    a = WordSubject.query.order_by(WordSubject.wordsubject).all()
    subject = []
    for i in range(len(a)):
        for j in range(10):
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
