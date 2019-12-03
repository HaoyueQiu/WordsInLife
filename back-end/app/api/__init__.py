from flask import Blueprint
'''
bluprint蓝图是实现模块化管理的一种方式，主要用于路由的管理，减少重复写url前缀
'''
bp = Blueprint('api', __name__)

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
from app.api import ping, users, tokens, words