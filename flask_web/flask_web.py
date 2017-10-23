import os
from flask import Flask,session,url_for,redirect,render_template
#from flask import flash
from flask_script import Manager,Shell
# from flask.ext.bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from datetime import datetime
from wtforms import StringField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('submit')

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s>' % self.username


# @app.route('/',methods=['POST','GET'])
# def hello_world():
#     form = NameForm()
#     if form.validate_on_submit():#表单提交后，如果数据能被所有验证函数接受，则返回True
#         old_name = session.get('name')
#         if old_name is not None and old_name != form.name.data:
#             flash('Looks like you have changed your name!')
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('hello_world'))
#     return render_template('index.html', form=form, name=session.get('name'))
    # return 'Hello World!'
    # return render_template('index.html',current_time = datetime.utcnow())

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('hello_world'))
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    #return 'Hello %s!' % name
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    # app.run()
    manager.run()
