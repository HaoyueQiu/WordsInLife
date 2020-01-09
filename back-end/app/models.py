import base64
import jwt
import os
from app import db
from datetime import datetime, timedelta
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'User'
    username = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    about_me = db.Column(db.Boolean())

    # token = db.Column(db.String(32), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)

    # 在打印的时候更好看，不会愚蠢的输出类的信息
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    '''
    todict和fromdict主要用于前后端交互，它们之间传递的是JSON对象。
    '''

    def to_dict(self, include_email=False):
        data = {
            'username': self.username,
            'name': self.name,
            'about_me': self.about_me,
        }

        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    '''
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    '''

    def get_jwt(self, expires_in=600):
        now = datetime.utcnow()
        # 将用户id和名称等信息作为payload加入token中
        payload = {
            'username': self.username,
            'name': self.name if self.name else self.username,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        # 使用jwt的加密算法进行加密
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            # 进行解密验证
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
            # 如果token过期那么就验证失败，否则就返回id
        except jwt.exceptions.ExpiredSignatureError as e:
            return None
        # return payload
        return User.query.get(payload.get('username'))

    # 由于jwt没办法回收，无法delete，所以不需要写revoke_jwt,只要等它自动过期即可，也因此有效时间不要设置的太长
    '''
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    '''


class WordSubject(db.Model):
    __tablename__ = 'WordSubject'
    wordsubject = db.Column(db.String(64), primary_key=True, index=True, unique=True)


class Word(db.Model):
    __tablename__ = 'Word'
    word = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    meaning = db.Column(db.String(64))
    # 外键，关联单词类别
    word_subject = db.Column(db.ForeignKey('WordSubject.wordsubject'))


class Game(db.Model):
    __tablename__ = 'Game'
    img_name = db.Column(db.String(64), primary_key=True, index=True, unique=True)
    # 外键，关联单词类别
    word_subject = db.Column(db.String(64), db.ForeignKey('WordSubject.wordsubject'))


class GameWord(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 存矩形范围
    x1 = db.Column(db.Integer, nullable=False)
    y1 = db.Column(db.Integer, nullable=False)
    x2 = db.Column(db.Integer, nullable=False)
    y2 = db.Column(db.Integer, nullable=False)
    word = db.Column(db.ForeignKey('Word.word'))
    game_img = db.Column(db.ForeignKey('Game.img_name'))

    def set_game_word(self, data):
        for field in ['x1', 'y1', 'x2', 'y2', 'word', 'game_img']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'word': self.word,
            'game_img': self.game_img,
        }
        return data


class UserWord(db.Model):
    __tablename__ = 'UserWord'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.ForeignKey('User.username'))
    word = db.Column(db.ForeignKey('Word.word'))
    proficiency = db.Column(db.Integer)
    times = db.Column(db.Integer)
    word_subject = db.Column(db.ForeignKey('WordSubject.wordsubject'))

    def set_attr(self, data):
        for field in ['user', 'word', 'proficiency', 'times', 'word_subject']:
            if field in data:
                setattr(self, field, data[field])


class UserFindError(db.Model):
    __tablename__ = 'UserFindError'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.ForeignKey('User.username'))
    errorText = db.Column(db.String(512))

    def set_error_text(self, data):
        for field in ['user', 'errorText']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'user': self.user,
            'errorText': self.errorText,
        }
        return data