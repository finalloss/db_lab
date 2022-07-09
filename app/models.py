# 模型定义
from datetime import date, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Book(db.Model):
    __tablename__ = 'Book'

    id = db.Column(db.Integer, primary_key=True)  # 图书编号，主键

    title = db.Column(db.String(100), nullable=False)  # 书名
    author = db.Column(db.String(80), nullable=False)  # 作者
    total = db.Column(db.Integer, nullable=False)  # 书的数量
    publisher = db.Column(db.String(50), nullable=False)  # 出版社
    type = db.Column(db.String(50), nullable=False)  # 类型
    img_name = db.Column(db.String(128), default='default_img.jpg')
    subarea_shelf = db.Column(db.String(50))  # 分区-书架号
    
    id_borrower = db.Column(db.Integer, db.ForeignKey('Borrower.id')) # 借阅人id

    def __repr__(self):
        return 'Book: %r' % self.title


class Admin(db.Model, UserMixin):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True)    # id

    name = db.Column(db.String(30), unique=True, nullable=False) # 姓名
    # email = db.Column(db.String(50), primary_key=True)  # email
    # phone = db.Column(db.String(20), unique=True)  # 电话
    is_admin = db.Column(db.Boolean, default=True) # tag
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'Admin: %r' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Borrower(db.Model, UserMixin):
    __tablename__ = 'Borrower'

    id = db.Column(db.Integer, primary_key=True, nullable=False)    # id

    email=db.Column(db.String(50), unique=True)  # 邮箱号
    ID_number = db.Column(db.String(20), unique=True, nullable=False)  # 身份证号
    name = db.Column(db.String(30), nullable=False) # 姓名
    number_of_viola = db.Column(db.Integer, nullable=False, default=0) # 违约次数
    phone = db.Column(db.String(20))  # 电话号
    is_admin = db.Column(db.Boolean, default=False) # tag
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return 'Borrower: %r' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Borrowing_record(db.Model):
    __tablename__ = 'Borrowing_record'

    id_borrower = db.Column(db.Integer, db.ForeignKey('Borrower.id'), primary_key=True) # 借阅人id
    id_book = db.Column(db.Integer, db.ForeignKey('Book.id'), primary_key=True) # 图书号

    borrowing_date = db.Column(db.Date, default=date.today()) # 借阅时间
    returning_date = db.Column(db.Date, default=date.today()+timedelta(days=21))  # 还书时间


class Booking_record(db.Model):
    __tablename__ = 'Booking_record'

    id_borrower = db.Column(db.Integer, db.ForeignKey('Borrower.id'), primary_key=True) # 借阅人id
    id_book = db.Column(db.Integer, db.ForeignKey('Book.id'), primary_key=True) # 图书号

    booking_date= db.Column(db.Date, default=date.today(), nullable=False) # 预约日期
    borrowing_date = db.Column(db.Date, default=date.today()+timedelta(days=5), nullable=False) # 应借书的日期
