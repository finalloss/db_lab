import os
import datetime
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone
from urllib.parse import urlparse, urljoin
from flask import request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/DBS_lab"
app.config['SECRET_KEY'] = "hard to guess"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + '/static/file/img'
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
dropzone = Dropzone(app)
# migrate = Migrate(app, db)
# bootstrap = Bootstrap(app)


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


# 保存图片，返回唯一的图片名
def img_upload(img):
    if not img:
        return None

    if img.filename.rsplit('.')[-1] not in ['jpg', 'png', 'gif', 'jpeg', 'gif']:
        return None

    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = str(nowtime) + str(img.filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(img_path)

    return filename


def redirect_back(backurl, **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(backurl, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


from app import models, views, errors, commands

