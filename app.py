from flask import url_for, Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from flask_bootstrap import Bootstrap5
from enum import Enum
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# ...
current_user ={'is_authenticated': False}
user = {'name': 'jervis'}
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user['is_authenticated']:
        return 'hello'
    else:
        return 'no'
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user, user=user, name=name, movies=movies)
@app.route('/hello')
def hello():
    return 'Hello'

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    print(url_for('user_page', name="jervis"))
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.root_path, 'db.sqlite')}'
# serve locally for faster and offline development
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'
db = SQLAlchemy(app)

class MyCategory(Enum):
    CAT1 = 'Category 1'
    CAT2 = 'Category 2'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(MyCategory), default=MyCategory.CAT1, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, unique=True)
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
with app.app_context():
        db.drop_all()
        db.create_all()
        for i in range(20):
            url = 'mailto:x@t.me'
            if i % 7 == 0:
                url = 'www.t.me'
            elif i % 7 == 1:
                url = 'https://t.me'
            elif i % 7 == 2:
                url = 'http://t.me'
            elif i % 7 == 3:
                url = 'http://t'
            elif i % 7 == 4:
                url = 'http://'
            elif i % 7 == 5:
                url = 'x@t.me'
            m = Message(
                text=f'Message {i + 1} {url}',
                author=f'Author {i + 1}',
                create_time=4321 * (i + 1)
            )
            if i % 2:
                m.category = MyCategory.CAT2
            if i % 4:
                m.draft = True
            db.session.add(m)
        user = User(name="jervis")
        m1 = Movie(title='My Neighbor', year='1989')
        m2 = Movie(title='Dead Poets Society', year='1990')
        db.session.add(user)
        db.session.add(m1)
        db.session.add(m2)

        for m in movies:
            movie = Movie(title=m['title'], year=m['year'])
            db.session.add(movie)
        db.session.commit()



@app.route('/icons')
def test_icons():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page=page, per_page=10)
    messages = pagination.items
    return render_template('icons.html', pagination=pagination, messages=messages,
                           current_user=current_user, user=user)