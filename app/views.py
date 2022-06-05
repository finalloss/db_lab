# 视图函数和对应的url的定义
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db
from app.models import Admin, Borrower, Book


# 在主页提供搜索功能
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    # 暂时只能搜书名
        book_title = request.form['book_title']
        all_book = Book.query.filter_by(title=book_title).all()
        return render_template('index.html', books=all_book)
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']

        if not id or not password:    # 若未输入id或密码
            flash('Invalid input.')
            return redirect(url_for('login'))

        # 验证id和密码是否正确
        user = Borrower.query.get(1)  # 从数据库中查询用户信息
        if user == None:
            user = Borrower.query.get(id)
        if user.validate_password(password):    # 验证成功
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页
        else:
            flash('Invalid id or password.')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面
        return render_template('login.html')
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
        name = request.form['name']
        password = request.form['password']
        if Borrower.query.filter_by(name=name).first() != None:   # 存在对应名字
            flash('Invalid name')
            return redirect(url_for('register'))  # 重定向到注册页面
        else:   # 不存在对应名字
            id = Borrower.query.count() + 1
            borrower = Borrower(id=id, name=name, number_of_viola=0)
            borrower.set_password(password)
            db.session.add(borrower)
            db.session.commit()
            flash('Register success, id='+str(id))
            return redirect(url_for('index'))  # 重定向到主页
    else:
        return render_template('register.html')


#@app.route('/borrow', methods=['GET', 'POST'])
#@login_required
#def borrow():
#    if request.method == 'POST':
#        title = request.form['book_title']
#
#        if not title: 
#            flash('Invalid input.')
#            return redirect(url_for('borrow'))
#
#        book = 
#        movie.title = title
#        movie.year = year
#        db.session.commit()
#        flash('Borrow success')
#        return redirect(url_for('index'))
#
#    return render_template('borrow.html')
#
