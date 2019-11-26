# coding=utf-8
from app import create_app, db

from app.models import User

'''
启动app
'''

app = create_app()


# 装饰器提供shell上下文项的函数
'''
装饰器:代码运行期间动态增加功能,而原函数不需要做代码改动的方式。
嵌套定义
def decoratorName
  def wrapper
@...使用 https://www.zhihu.com/question/26930016
'''
@app.shell_context_processor
def make_shell_context():
    # dict(db=db, User=User)
    # 另一种书写方式，初始化dict
    return {'db': db, 'User': User}
