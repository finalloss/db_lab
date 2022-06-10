# 视图函数和对应的url的定义
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, and_
from re

from app import app, db
from app.models import Admin, Borrower, Book


# 在主页提供搜索功能
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    # 暂时只能搜书名
        keyword = request.form['keyword']
        books = Book.query.all()
        pt = '.*' + str(keyword) + '.*'
        for book in books:
            if re.search(pt, books.title) == None:  # 即书名与关键词对应模式串匹配
                books.remove(book)
        return redirect(url_for('search_result', books=books))
    else:
        return render_template('index.html')


# 几个处理注册、登录的视图函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        # remember = request.form['rememberme']

        if id == '' or password == '':    # 若未输入id或密码
            flash('Invalid input.')
            return redirect(url_for('login'))

        # 验证id和密码是否正确
        admin = Admin.query.get(id)  # 从数据库中查询用户信息
        borrower = Borrower.query.get(id)  # 从数据库中查询用户信息
        if admin != None:   # 判断是管理员还是读者
            user = admin
        elif borrower!= None:
            user = borrower
        else:
            flash("Invalid id")
            return redirect(url_for('login'))

        if user.validate_password(password):    # 验证成功
            login_user(user)  # 登入用户
            if user.is_admin:
                flash('管理员'+ str(user.name) +'成功登录')
            else:
                flash('读者'+ str(user.name) + '成功登录')
            return redirect(url_for('index'))  # 重定向到主页
        else:
            flash('Invalid password.')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面

    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出当前用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/register', methods=['GET', 'POST']) # 借阅人注册
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        ID_number = request.form['ID_number']
        phone = request.form['phone']
        password = request.form['password']
        if Borrower.query.filter(or_(Borrower.email==email, Borrower.ID_number==ID_number)).first() != None:   # email或身份证号重复
            flash('Invalid email or ID number')
            return redirect(url_for('register'))  # 重定向到注册页面
        else:   
            id = Borrower.query.count() + 10001
            borrower = Borrower(email=email, id=id, ID_number=ID_number, name=name, phone=phone, number_of_viola=0)
            borrower.set_password(password)
            db.session.add(borrower)
            db.session.commit()
            flash('Register success, id='+str(id))
            return redirect(url_for('index'))  # 重定向到主页
    else:
        return render_template('register.html')


# 图书主页，读者可以通过图书主页预约图书，管理员可以修改图书信息
@app.route('/book/<int:book_id>/index', methods=['POST'])
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)


# 执行预约图书的操作
@app.route('/book/<int:book_id>/booking', methods=['POST'])
@login_required
def book_book(book_id, borrower_id):
    book = Book.query.get_or_404(book_id)
    booking_record = Booking_record(id_borrower=borrower_id, id_book=borrower_id)
    db.session.add(booking_record)
    db.session.commit()
    flash('booking successfully')
    return redirect(url_for('/book/<int:book_id>/book'))


# 读者有个人主页，可以通过个人主页查看借阅和预约的图书，也可以取消预约
@app.route('/borrower/index', methods=['GET'])
@login_required
def borrower():
    return render_template('borrower.html')


# 执行取消预约操作
@app.route('/book/<int:book_id>/unbooking', methods=['POST'])
@login_required
def unbook(book_id, borrower_id):
    booking_record = Booking_record(id_borrower=borrower_id, id_book=borrower_id)
    db.session.delete(booking_record)
    db.session.commit()
    flash('unbooking successfully')
    return redirect(url_for('index'))


# 管理员可以增加新的图书，暂时没有其他导入图书的接口
@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.methed == 'POST':
        id = Book.query.count() + 1
        B = Book(id=id, title=request.form['title'], author=request.form['author'], total=request.form['total'], publisher=request.form['publisher'], type=request.form['type'], subarea_shelf=request.form['subarea_shelf'])
        db.session.add(B)
        db.session.commit()
        flash('adding book successfully')
    else:
        return render_template('add_book.html')


# 管理员可以修改已有图书信息
@app.route('/book/<int:book_id>/alter', methods=['POST'])
@login_required
def alter_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    B = Book(id=book_id, title=request.form['title'], author=request.form['author'], total=request.form['total'], publisher=request.form['publisher'], type=request.form['type'], subarea_shelf=request.form['subarea_shelf'])
    db.session.add(B)
    db.session.commit()
    flash('book altered')
    return redirect(url_for('book'))


# 返回查询结果，即对应图书信息
@app.route('/search_result', methods=['GET', 'POST'])
def search_result():
    keyword = request.form['keyword']
    books = Book.query.all()
    pt = '.*' + str(keyword) + '.*'
    for book in books:
        if re.search(pt, books.title) == None:  # 即书名与关键词对应模式串匹配
            books.remove(book)
    return render_template('search_result.html', books=books)
