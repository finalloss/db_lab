# 视图函数和对应的url的定义
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_, and_
import re

from app import app, db, img_upload, redirect_back
from app.models import Admin, Borrower, Book, Borrowing_record, Booking_record


# 在主页提供搜索功能
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    # 暂时只能搜书名
        keyword = request.form['keyword']
        return redirect(url_for('search_result', keyword=keyword))
    else:
        return render_template('index.html')


# 返回查询结果，即对应图书信息
@app.route('/search/result/<keyword>', methods=['GET', 'POST'])
def search_result(keyword):
    # 分页
    page = request.args.get('page', default=1, type=int)
    pagination = Book.query.filter(Book.title.like('%' + str(keyword) + '%')).order_by(Book.id)\
            .paginate(page, per_page=5, error_out=False)
    books = pagination.items

    if request.method == 'POST':
        # 分页
        keyword = request.form['keyword']
        if request.form.get('type') != "书籍类型":
            type = request.form.get('type')
            pagination = Book.query.filter(and_(Book.title.like('%' + str(keyword) + '%'), Book.type==type)).paginate(page, per_page=5, error_out=False)
        else:
            pagination = Book.query.filter(Book.title.like('%' + str(keyword) + '%')).paginate(page, per_page=5, error_out=False)

        page = request.args.get('page', default=1, type=int)
        books = pagination.items

        return render_template('search_result.html', pagination=pagination, books=books, keyword=keyword)
    else:
        return render_template('search_result.html', pagination=pagination, books=books, keyword=keyword)


# 处理登录
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


# 忘记密码
@app.route('/passwordreset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        ID_number = request.form['ID_number']
        phone = request.form['phone']
        password = request.form['password']

        borrower = db.session.query(Borrower).filter(and_(Borrower.email==email, Borrower.name==name,\
                Borrower.ID_number==ID_number, Borrower.phone==phone)).first()
        if borrower == None:
            flash('personal information not found')
            render_template('passwordreset.html')
        else:
            pass

        borrower.set_password(password)
        db.session.commit()
        flash('password reset')
        return redirect(url_for('login'))
    else:
        return render_template('passwordreset.html')


# 登出
@app.route('/logout', methods=['GET'])
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出当前用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


# 借阅人注册
@app.route('/register', methods=['GET', 'POST'])
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
@app.route('/book/<int:book_id>', methods=['GET','POST'])
def exact_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('bookexact.html', book=book)


# 执行预约图书的操作
@app.route('/book_book/<int:book_id>/<int:borrower_id>', methods=['POST'])
@login_required
def book_book(book_id, borrower_id):
    book = Book.query.get_or_404(book_id)
    booking_record = Booking_record(id_borrower=borrower_id, id_book=book_id)

    if book.total == 0:
        flash('no enough book')
    elif Booking_record.query.get((borrower_id, book_id)) != None:
        flash('不能重复预约！')
    else:    
        book.total = book.total - 1
        db.session.add(booking_record)
        db.session.commit()
        flash('booking successfully')

    return redirect_back('/book_book/'+str(book_id)+'/'+str(borrower_id))


# 执行取消预约操作
@app.route('/unbook/<int:book_id>/<int:borrower_id>', methods=['POST'])
@login_required
def unbook(book_id, borrower_id):
    book = Book.query.get_or_404(book_id)
    if Booking_record.query.get_or_404((borrower_id, book_id)) == None:
        flash('booking record not found')
    else:
        booking_record = Booking_record.query.get((borrower_id, book_id))
        book.total = book.total + 1
        db.session.delete(booking_record)
        db.session.commit()
        flash('unbooking successfully')

    return redirect_back('/unbook/'+str(book_id)+'/'+str(borrower_id))


# 读者有个人主页，可以通过个人主页查看借阅和预约的图书等信息
@app.route('/personal-page/<int:borrower_id>', methods=['GET'])
@login_required
def personal_page(borrower_id):
    bor_results =  db.session.query(Book, Borrower, Borrowing_record).filter(and_(Book.id==Borrowing_record.id_book, \
            Borrower.id==Borrowing_record.id_borrower, Borrower.id==borrower_id)).all()
    boo_results =  db.session.query(Book, Borrower, Booking_record).filter(and_(Book.id==Booking_record.id_book, \
            Borrower.id==Booking_record.id_borrower, Borrower.id==borrower_id)).all()
    borrower = db.session.query(Borrower).filter(Borrower.id == borrower_id).all()
    return render_template('borrower.html',borrower = borrower, bor_results=bor_results, boo_results=boo_results)


# 管理员有个人主页，可以通过个人主页查看借阅和预约的图书等信息
@app.route('/admin-page/<int:admin_id>', methods=['GET'])
@login_required
def admin_page(admin_id):
    bor_results = db.session.query(Book, Borrower, Borrowing_record).filter(and_(Book.id==Borrowing_record.id_book, \
            Borrower.id==Borrowing_record.id_borrower)).all()
    boo_results = db.session.query(Book, Borrower, Booking_record).filter(and_(Book.id==Booking_record.id_book, \
            Borrower.id==Booking_record.id_borrower)).all()
    admin = db.session.query(Admin).filter(Admin.id==admin_id).all()
    return render_template('admin_page.html', admin=admin, bor_results=bor_results, boo_results=boo_results)


# 管理员可以增加新的图书，暂时没有其他导入图书的接口
@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        img = request.files['image']
        img_name = img_upload(img)
        if img_name == None:
            return 'invalid image', 400
        else:
            pass

        id = Book.query.count() + 1

        B = Book(id=id, title=request.form['title'], author=request.form['author'], total=request.form['total'], \
                publisher=request.form['publisher'], type=request.form['type'], subarea_shelf=request.form['subarea_shelf'],\
                 img_name=img_name)
        db.session.add(B)
        db.session.commit()
        flash('adding book successfully')
        return redirect(url_for('add_book'))
    else:
        return render_template('add_book.html')


# 管理员可以修改已有图书信息
@app.route('/book/<int:book_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        db.session.delete(book)

        img = request.files['image']
        img_name = img_upload(img)
        if img_name == None:
            return 'invalid image', 400
        else:
            pass

        total = book.total
        B = Book(id=book_id, title=request.form['title'], author=request.form['author'], total=total, publisher=\
                request.form['publisher'], type=request.form['type'], subarea_shelf=request.form['subarea_shelf'],\
                img_name=img_name)
        db.session.add(B)
        db.session.commit()
        flash('book edited')
        return redirect(url_for('exact_book', book_id=book_id))
    else:
        return render_template('edit_book.html', book=book)


# 执行删除图书的操作
@app.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('book deleted')
    return redirect_back('/deleteBook/'+str(book_id))

@app.route('/guideadmin', methods=['GET', 'POST']) # 借阅人注册
def guideadmin():
    return render_template('guideadmin.html')

@app.route('/guide', methods=['GET', 'POST']) # 借阅人注册
def guide():
    return render_template('guide.html')
