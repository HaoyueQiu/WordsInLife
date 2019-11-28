import base64
import jwt
import os
from app import db
from datetime import datetime, timedelta
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash


# 用于分页
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码

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
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        # 只有当用户请求自己的数据时才包含 email
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
            'user_id': self.id,
            'name': self.username,
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
        return User.query.get(payload.get('user_id'))
    # 由于jwt没办法回收，无法delete，所以不需要写revoke_jwt,只要等它自动过期即可，也因此有效时间不要设置的太长

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    '''
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    '''
