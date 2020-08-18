"""
@file: config.py
@author：wang
@time: 2020/8/14 0014 9:05
"""
# 配置文件
import os


class Config:
    base_dir = os.path.abspath(os.path.dirname(__name__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'sqlite3.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
