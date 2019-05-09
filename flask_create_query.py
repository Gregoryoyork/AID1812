import datetime,os,pymysql

import math
from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from sqlalchemy import or_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@localhost:3306/jump"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['DEBUG']=True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)
manager = Manager(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class Ajax(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    age = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(120),nullable=True)
    password = db.Column(db.String(100),nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    isActive = db.Column(db.Boolean,default=True)


@app.route('/01-file',methods=['GET','POST'])
def file_views():
    if request.method == 'GET':
        return render_template('01-file.html')
    else:
        picture = request.files['picture']
        ext = picture.filename.split('.')[-1]
        ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = ftime + '.' + ext
        basedir = os.path.dirname(__file__)
        totalPath = os.path.join(basedir,'static/download',filename)
        print(totalPath)
        picture.save(totalPath)
        # picture.save('/home/tarena/aid1812/Flask/reviewagain/static/'+filename)
        return 'ok'

@app.route('/01-add')
def add_views():
    user = Users()
    user.name = 'Gregoryo'
    user.age = 20
    user.email = 'Gregoryo@163.com'


    db.session.add(user)
    db.session.commit()
    # ajax = Ajax()
    # ajax.name = 'jack'
    # ajax.age = 25
    # ajax.email = 'jack@16.com'
    # ajax.url = 'www.jack.com'
    # ajax.password = '123456'
    # db.session.add(ajax)
    return 'OK'

@app.route('/register',methods=['GET','POST'])
def register_views():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        ajax = Ajax()
        ajax.name = request.form.get('name')
        ajax.age = request.form.get('age')
        ajax.email = request.form.get('email')
        ajax.url = request.form.get('url')
        ajax.password = request.form.get('password')
        db.session.add(ajax)

        return 'OK'

@app.route('/reg',methods=['GET','POST'])
def reg_views():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        user = Users()
        user.name = request.form.get('name')
        user.age = request.form.get('age')
        user.email = request.form.get('email')
        user.isActive = False
        if 'isActive' in request.form:
            user.isActive = True
        db.session.add(user)
        return 'OK'

@app.route('/login',methods=['GET','POST'])
def login_views():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        user = db.session.query(Ajax).filter_by(name=name,password=password).first()
        if user:
            return "<script>alert('OK');location.href='http://www.baidu.com'</script>"
        else:
            return "<script>alert('NOT OK');location.href='/login';</script>"

@app.route('/query')
def query_views():
    kw = request.args.get('kw')
    if kw:
        users = db.session.query(Users).filter(
            or_(
                Users.name.like('%'+kw+'%'),
                Users.email.like('%'+kw+'%')
                )
        ).all()
    else:
        users = db.session.query(Users).all()
    return render_template('query.html',users=users,kw=kw)



#=============got===you=============down=already====================================================
@app.route('/01-page')
def page_views():
    pageSize = 2
    page = int(request.args.get('page','1'))
    ost = (page-1)*pageSize
    users = db.session.query(Users).offset(ost).limit(pageSize).all()
    totalCount = db.session.query(Users).count()
    lastPage = math.ceil(totalCount/pageSize)

    #上一页prevPage和下一页nextPage
    prevPage = 1
    if page > 1:
        prevPage = page - 1

    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1


    return render_template('01-page.html',users=users,lastPage=lastPage,nextPage=nextPage,
                           prevPage=prevPage)




if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()