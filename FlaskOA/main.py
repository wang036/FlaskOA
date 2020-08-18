"""
@file: main.py
@author：wang
@time: 2020/8/14 0014 9:05
"""
from flask_migrate import Migrate, MigrateCommand

from config import Config
from oa import create_app, db
from flask_script import Manager, Command

app = create_app(Config)

# 2、创建Manager对象
manager = Manager(app)

# 创建Migrate对象
migrate = Migrate(app, db)


# 5、创建子类
class Hello(Command):
    def run(self):
        print('hello')
        # 设置debug模式，运行 python main.py hello


class Runserver(Command):
    def run(self):
        # flask服务启动  监听8000 端口
        app.run( debug=True)


# 6、添加命令
manager.add_command('runserver', Runserver())
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    # db.create_all(app=app)
    # app.run(debug=True)

    # 3、启动
    manager.run()
    # 4、运行  python main.py runserver
