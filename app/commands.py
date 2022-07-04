import click
from app import app, db
from app.models import Admin, Book, Booking_record, Borrowing_record, Borrower


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('database initialized')


@app.cli.command()
def forge():
    """Generate fake book data."""
    books = [{'id':1, 'title':'数据库系统概论', 'author':'王珊', 'total':20, 'publisher':'高等教育出版社', 'type':'数理', 'subarea_shelf':'西区中文书库 TP311.13/189'},
            {'id':2, 'title':'三体-死神永生', 'author':'刘慈欣','total':15, 'publisher':'重庆出版社', 'type':'文学', 'subarea_shelf':'西区中文书库 I247.55/44'},
        {'id': 3, 'title': '数学分析', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 4, 'title': '线性代数', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 5, 'title': '红与黑', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 6, 'title': '战争与和平', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 7, 'title': '1984', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 8, 'title': '1Q84', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 9, 'title': '数据挖掘导论', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 10, 'title': '人工智能基础', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 11, 'title': '三生三世十里桃花', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 12, 'title': '红与黑的碰撞-决死', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '文学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 13, 'title': '苏菲的世界', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 14, 'title': '枪炮、病菌与钢铁', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '历史',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 15, 'title': '风神巴巴托斯的歌唱', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 16, 'title': '喻神泽被众生', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 17, 'title': '圣经', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 18, 'title': '神论', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 19, 'title': '国富论', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '经济',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 20, 'title': '去码头整点薯条', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '哲学',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 21, 'title': '运筹学', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 22, 'title': '离散数学', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 23, 'title': '随机过程', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 24, 'title': '数理逻辑', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 25, 'title': '量子物理新话', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
        {'id': 26, 'title': '数学之美', 'author': '刘慈欣', 'total': 15, 'publisher': '重庆出版社', 'type': '数理',
         'subarea_shelf': '西区中文书库 I247.55/44'},
    ]
    for book in books:
        B = Book(id=book['id'], title=book['title'], author=book['author'], total=book['total'], publisher=book['publisher'], type=book['type'], subarea_shelf=book['subarea_shelf'])
        db.session.add(B)

    borrower = Borrower(id=10001, email='zjyang@mail.ustc.edu.cn', name='yzj', ID_number='123',phone='4653516354')
    borrower.set_password('123456')
    db.session.add(borrower)
    db.session.commit()

    bor_record = Borrowing_record(id_book=1, id_borrower=10001)
    bor_record_1 = Borrowing_record(id_book=2, id_borrower=10001)
    booking_record = Booking_record(id_book=2, id_borrower=10001)
    db.session.add(bor_record)
    db.session.add(bor_record_1)
    db.session.add(booking_record)
    db.session.commit()

    click.echo('Done.')


@app.cli.command()
@click.option('--name', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(name, password):
    db.create_all()
    admin_num = Admin.query.count() + 1
    click.echo('Creating admin, id = ' + str(admin_num))
    admin = Admin(name=name, id=admin_num)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()
    click.echo('Done.')
