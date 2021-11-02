from flask import Flask,render_template,redirect,url_for,flash,request,abort,send_file
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import Information,StudentRegister,Login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import csv
from smtplib import SMTP

app = Flask(__name__)

EMAIL = 'donotreplyepicuniv@gmail.com'
PASSWORD = 'donotreplyepicuniv12'
app.config['SECRET_KEY'] = 'allyouwannadoiscocohangingoutwithyouisnogo'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///DBMS.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

def csv_data(data):
    csv_datas = data
    with open(f"list.csv", 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_datas)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.Email == 'priyanshuc4423@gmail.com' and current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return abort(403,description="Your dont have credibility")

    return decorated_function

@admin_only
@login_required
@app.route('/download')
def download():
    return send_file('list.csv')





class StudentForms(db.Model):
    __tablename__ = "Studentforms"
    pinnumber = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    Fathername= db.Column(db.String(250), nullable=False)
    Fathernumber = db.Column(db.String(250), nullable=False)
    Mothername = db.Column(db.String(250), nullable=False)
    Mothernumber = db.Column(db.String(250), nullable=False)
    number = db.Column(db.String(250), nullable=False)
    alternatenumber = db.Column(db.String(250), nullable=False)
    tenboard = db.Column(db.String(250), nullable=False)
    tenmarks = db.Column(db.String(250), nullable=False)
    twelveboard = db.Column(db.String(250), nullable=False)
    twelvemarks= db.Column(db.String(250), nullable=False)
    dt = db.Column(db.String(250), nullable=False)
    branch = db.Column(db.String(250), nullable=False)
    course = db.Column(db.String(250),nullable = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.pinnumber'))


class User(UserMixin,db.Model):
    __tablename__ = "user"
    pinnumber = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(250),nullable = False)
    Email = db.Column(db.String(250),nullable = False,unique = True)
    password = db.Column(db.String(250),nullable = False)
    studentforms = relationship("StudentForms", backref="user", uselist=False)
    def get_id(self):
        return (self.pinnumber)

db.create_all()



@login_manager.user_loader
def load_user(user_pinnumber):
    return User.query.get(int(user_pinnumber))

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        contacted = True
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        print(name,email,subject,message)
        with SMTP('smtp.gmail.com', 587, timeout=180) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            message = f"Subject:{subject}\n\n{name} his email id {email}\n {message}"
            connection.sendmail(from_addr=EMAIL, to_addrs='priyanshuc4423@gmail.com', msg=message)
        return render_template('index.html',contacted = contacted)
    if request.method == 'GET':
        contacted = False
        return render_template('index.html', contacted=contacted)

@app.route("/admin",methods = ['GET','POST'])
@login_required
@admin_only
def data():
    form = db.session.query(StudentForms).all()
    csv_datas = [['PINNUMBER','name', 'age', 'gender', 'email', 'FATHERNAME', 'FATHERNUMBER','MOTHERNAME','MOTHERNUMBER','NUMBER','ALTERNATENUMBER','TENBOARDS','TENBOARD','TEWELVEBOARD','twelvemarks','dt','branch','course']]
    for data in form:
        csv_datas.append([data.pinnumber,data.name,data.age,data.gender,data.email,data.Fathername,data.Fathernumber,data.Mothername,data.Mothernumber,data.alternatenumber,data.number,data.tenmarks,data.tenboard,data.twelveboard,data.twelvemarks,data.dt,data.branch,data.course])
    csv_data(csv_datas)


    return render_template('data.html',form =form)


@login_required
@app.route('/information',methods = ['GET','POST'])
def information():
    data = User.query.filter_by(pinnumber=current_user.pinnumber).first()
    form = Information(
        pinnumber = data.pinnumber,
        name = data.name,
        email = data.Email
    )
    if StudentForms.query.filter_by(pinnumber = current_user.pinnumber).first():
        return redirect(url_for('home'))
    if form.validate_on_submit():
        studentform = StudentForms(
            pinnumber = form.pinnumber.data,
            name = form.name.data,
            age = form.age.data,
            gender = form.gender.data,
            email = form.email.data,
            Fathername = form.Fathername.data,
            Fathernumber = form.FatherNumber.data,
            Mothername = form.Mothername.data,
            Mothernumber = form.MotherNumber.data,
            number = form.number.data,
            alternatenumber = form.Alternatenumber.data,
            tenboard = form.tenboard.data,
            tenmarks = form.tenmarks.data,
            twelveboard = form.twelveboard.data,
            twelvemarks = form.twelevemarks.data,
            dt = form.dt.data,
            branch = form.branch.data,
            course = form.course.data,
            parent_id = current_user.pinnumber,
        )
        db.session.add(studentform)
        db.session.commit()
        with SMTP('smtp.gmail.com', 587, timeout=180) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            message = f"Subject:DONTREPLY APPLICATION RECIEVED\n\nThank you {form.name.data}\n we will get back to you as soon as possible till then HUSTLE ON!!! "
            connection.sendmail(from_addr=EMAIL, to_addrs=f"{form.email.data}", msg=message)
        return redirect(url_for('home'))







    return render_template('register.html',form = form)


@app.route('/register',methods =['GET','POST'])
def register():
    form = StudentRegister()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        if form.password.data == form.another_password.data:
            email = form.email.data
            user = User.query.filter_by(Email = email).first()
            if user:
                flash('THIS EMAIL ALEARDY EXIST')
                return render_template('login.html',form = form)
            with open("pinnumber.txt", mode="r") as file:
                pinnumber = int(file.read())

            pinnumber = pinnumber + 1

            with open('pinnumber.txt',mode='w') as file:
                file.write(str(pinnumber))

            password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            data = User(pinnumber = pinnumber,name = form.name.data,Email = form.email.data,password = password)
            db.session.add(data)
            db.session.commit()
            login_user(data)

            return redirect(url_for('home'))
    return render_template('register.html',form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        data = User.query.filter_by(Email=form.email.data).first()
        if data:
            if check_password_hash(data.password, form.password.data):
                login_user(data)
                return redirect(url_for('home'))
            else:
                flash('INVALID PASSWORD', 'error')
                return redirect(url_for('login'))
        else:
            flash('THE USER ID DOESNT EXIST', 'error')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@login_required
@app.route('/logout',methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/home')
def home():
    name = current_user.name
    return render_template('home.html',name = name,current_user = current_user)

@app.route('/about',methods = ['GET','POST'])
def about():
    return render_template('about.html')


@admin_only
@login_required
@app.route('/statistic')
def stats():
    male = StudentForms.query.filter_by(gender = 'MALE')
    female = StudentForms.query.filter_by(gender = 'FEMALE')
    labels = ['male','female']
    print(female.count())
    values = [male.count(), female.count()]
    print(values)
    course_BBA = StudentForms.query.filter_by(course = 'BBA')
    course_BTECH = StudentForms.query.filter_by(course = 'BTECH')
    course_BCOM = StudentForms.query.filter_by(course = 'BCOM')
    twelveboard_CBSE = StudentForms.query.filter_by(twelveboard = 'CBSE')
    twelveboard_ICSE = StudentForms.query.filter_by(twelveboard = 'ICSE')
    twelveboard_STATE = StudentForms.query.filter_by(twelveboard = 'SSC')
    labels_board = ['CBSE','ICSE','SSC']
    labels_course = ['BBA','BTECH','BCOM']
    values_board = [twelveboard_CBSE.count(),twelveboard_ICSE.count(),twelveboard_STATE.count()]
    values_course = [course_BBA.count(),course_BTECH.count(),course_BCOM.count()]
    return render_template('stastic.html',labels_gender=labels,values_gender=values,labels_course=labels_course,values_course=values_course,labels_board = labels_board,values_board = values_board)
if __name__ == '__main__':
    app.run(debug=True)