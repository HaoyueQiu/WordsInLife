import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
"""
dotenv就是一个能使得node.js从文件中加载环境变量的库，
通过它我们只需要将程序的环境变量写在.env这个文件里
"""
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    #配置数据哭
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False