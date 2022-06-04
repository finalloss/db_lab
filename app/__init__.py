import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/DBS_lab"
app.config['SECRET_KEY'] = "hard to guess"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'   # 访问一些页面时，将未登录用户重定向到登录页面
login_manager.login_message = '请登录'  # 同时显示提示信息
@login_manager.user_loader
def load_user(user_id):
    return None

# migrate = Migrate(app, db)
# bootstrap = Bootstrap(app)


from app import models, views, errors, commands

