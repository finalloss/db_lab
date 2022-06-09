import click
from app import app, db
from app.models import Admin, Book


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
    books = [
            {'id':1, 'title':'数据库系统概论', 'author':'王珊', 'total':20, 'publisher':'高等教育出版社', 'type':'数据库系统-概论-高等学校-教材', 'subarea_shelf':'西区中文书库 TP311.13/189'},
            {'id':2, 'title':'三体', 'author':'刘慈欣','total':15, 'publisher':'重庆出版社', 'type':'科学幻想小说-中国-当代', 'subarea_shelf':'西区中文书库 I247.55/44'}
    ]
    for book in books:
        B = Book(id=book['id'], title=book['title'], author=book['author'], total=book['total'], publisher=book['publisher'], type=book['type'], subarea_shelf=book['subarea_shelf'])
        db.session.add(B)
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
