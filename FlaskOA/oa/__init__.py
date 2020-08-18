"""
@file: __init__.py
@author：wang
@time: 2020/8/14 0014 9:06
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from oa.user.views import ubp
    app.register_blueprint(ubp)
    return app
