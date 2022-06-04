# 模型定义
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Book(db.Model):
    __tablename__ = 'Book'
    id = db.Column(db.Integer, primary_key=True) # 图书编号，主键
    title= db.Column(db.String(100), nullable=False) # 书名
    author = db.Column(db.String(80), nullable=False)# 作者

    def __repr__(self):
        return 'Book %r' % self.title


class Admin(db.Model, UserMixin):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True) # 图书管理员编号，主键
    name = db.Column(db.String(30), nullable=False) # 姓名
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    
class Borrower(db.Model, UserMixin):
    __tablename__ = 'Borrower'
    id = db.Column(db.Integer, primary_key=True) # 借阅人id，主键
    name = db.Column(db.String(30), nullable=False) # 姓名
    number_of_viola = db.Column(db.Integer, nullable=False) # 违约次数
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Borrowing_record(db.Model):
    __tablename__ = 'Borrowing_record'
    id = db.Column(db.Integer, primary_key=True) # 借阅记录号，主键

#    id_borrower = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=False) # 借阅人号
#    id_book = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False) # 图书号


# class Borrowing_card(db.Model):
#     id = db.Column(db.Integer, primary_key=True) # 借阅证号，主键
#     status = db.Column(db.Boolean, nullable=False)  # 借阅证状态
#     number_of_viola = db.Column(db.Integer, nullable=False) # 违约次数
# 
#     id_borrower = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=False) # 借阅人号


class Appointment_record(db.Model):
    __tablename__ = 'Appointment_record'
    id = db.Column(db.Integer, primary_key=True) # 预约记录号，主键
    date_to_return = db.Column(db.Date, nullable=False) # 还书日期
    date_to_borrow = db.Column(db.Date, nullable=False) # 借书日期

#    id_borrower = db.Column(db.Integer, db.ForeignKey('Borrower.id'), nullable=False) # 借阅人号
#    id_book = db.Column(db.Integer, db.ForeignKey('Book.id'), nullable=False) # 图书号

