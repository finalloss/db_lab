import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/DBS_lab"
app.config['SECRET_KEY'] = "hard to guess"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + '/static/file/img'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


login_manager.login_view = 'index'   # 在未登录用户访问受保护的页面时，将其重定向到主页
login_manager.login_message = '请登录'  # 同时显示提示信息


@login_manager.user_loader
def load_user(user_info):
    from app.models import Admin, Borrower
    admin = Admin.query.get(user_info)  # 按照主键查询
    borrower = Borrower.query.get(user_info)
    if admin != None:
        return admin
    else:
        return borrower



# migrate = Migrate(app, db)
# bootstrap = Bootstrap(app)


from app import models, views, errors, commands

