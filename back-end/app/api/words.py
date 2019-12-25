from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import WordSubject, Word, UserWord
from flask import request
from functools import cmp_to_key


def words_subject_compare(x, y):
    # 已经完全背完了
    if x['complete_ratio'] == 100:
        return 1
    elif y['complete_ratio'] == 100:
        return -1
    # 还没有背过的单词
    elif x['is_add_to_plan'] == False:
        return 1
    elif y['is_add_to_plan'] == False:
        return -1
    # 背过一些的单词，背的越少比例的放在越下面
    elif x['complete_ratio'] < y['complete_ratio']:
        return 1
    else:
        return -1



@bp.route('/wordSubject', methods=['GET'])
def get_words_subject():
    username = request.args.get('username')
    a = WordSubject.query.all()
    subject = []
    for i in range(len(a)):
        wordsubject = a[i].wordsubject
        words_memorized = len(UserWord.query.filter(UserWord.user == username, UserWord.proficiency >= 1,
                                                    UserWord.word_subject == wordsubject).all())
        words_memorizing = len(UserWord.query.filter(UserWord.user == username, UserWord.times > 0,
                                                     UserWord.word_subject == wordsubject).all())
        words_size = len(Word.query.filter_by(word_subject=wordsubject).all())
        print(words_size, words_memorizing)
        # print(wordsubject,username,words_memorized)
        is_add_to_plan = True
        if words_memorizing:
            words_complete_ratio = int(100 * words_memorized / words_size)
        else:
            words_complete_ratio = 0
            is_add_to_plan = False
        subject.append(
            {'wordsubject': wordsubject, 'complete_ratio': words_complete_ratio, 'is_add_to_plan': is_add_to_plan})

    subject = sorted(subject,key=cmp_to_key(words_subject_compare))
    print(subject)
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
        queryB = UserWord.query.filter_by(user=username, word=a[i].word).all()
        if len(queryB) == 0 or queryB[0].proficiency < 1:
            if (len(queryB) == 0):
                user_word = UserWord()
                attr = {}
                attr['user'] = username
                attr['word'] = a[i].word
                attr['proficiency'] = 0
                attr['times'] = 0
                attr['word_subject'] = wordsubject
                user_word.set_attr(attr)
                db.session.add(user_word)
                db.session.commit()
            queryB = UserWord.query.filter_by(user=username, word=a[i].word).all()
            words.append(
                {'EN': a[i].word, 'CN': a[i].meaning, 'proficiency': queryB[0].proficiency, 'times': queryB[0].times})
    # print(words)
    return jsonify(words)


@bp.route('/words', methods=['POST'])
def save_word_proficiency():
    data = request.get_json()
    words = data.get('words')
    username = data.get('username')
    print(words)
    for i in range(1, len(words)):
        user_word = UserWord.query.filter_by(user=username, word=words[i]['EN']).first()
        user_word.proficiency = words[i]['proficiency']
        user_word.times = words[i]['times']
        db.session.commit()
    # save data in sql
    return jsonify({'info': 'correct!'})




