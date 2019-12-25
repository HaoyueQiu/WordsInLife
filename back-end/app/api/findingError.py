from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import UserFindError
from flask import request


# 提交错误
@bp.route('/findingError', methods=['POST'])
def add_error():
    data = request.get_json()
    username = data.get('username')
    errorText = data.get('errorText')


    user_find_error = UserFindError()
    attr = {}
    attr['errorText'] = errorText
    attr['user'] = username

    user_find_error.set_error_text(attr)
    db.session.add(user_find_error)
    db.session.commit()
    response = jsonify(user_find_error.to_dict())
    response.status_code = 201
    return response


