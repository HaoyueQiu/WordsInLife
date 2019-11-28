import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
"""
dotenv就是一个能使得node.js从文件中加载环境变量的库，
通过它我们只需要将程序的环境变量写在.env这个文件里
"""
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    #配置数据k库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #配置pyjwt
    '''
    用户认证授权，原先使用flask-httpAuth实现的token功能，前端用户登录后不清楚自己的用户id，因此无法获取自己的信息。
    所以改用jwt库，它允许在token中添加一些不是隐私数据的payload。
    https://www.thatyou.cn/flask-pyjwt-%E5%AE%9E%E7%8E%B0%E5%9F%BA%E4%BA%8Ejson-web-token%E7%9A%84%E7%94%A8%E6%88%B7%E8%AE%A4%E8%AF%81%E6%8E%88%E6%9D%83/
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'