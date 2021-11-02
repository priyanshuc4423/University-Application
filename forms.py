from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, SubmitField, PasswordField,SelectField,DateField
from wtforms.validators import DataRequired, URL,email_validator,Length,Email



class Information(FlaskForm):
    pinnumber = StringField('Pin Number', validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    age = StringField('Age',validators=[DataRequired()])
    gender = SelectField(label='GENDER',choices=['MALE','FEMALE'],validators=[DataRequired()],render_kw={'placeholder':'Department'})
    email = StringField(label='email',validators=[DataRequired(),Email(message='please enter valid email id')])
    Fathername = StringField(label='Father name')
    FatherNumber = StringField(label='Father number',validators=[Length(min=10,max=10)])
    Mothername = StringField(label='Mother name')
    MotherNumber = StringField(label='Mother number',validators=[Length(min=10,max=10)])
    number = StringField(label="Number",validators=[DataRequired(),Length(min=10,max=10)])
    Alternatenumber = StringField(label='alternate number',validators=[DataRequired(),Length(min=10,max=10)])
    tenboard = SelectField(label='Class 10th Board',choices=['CBSE','ICSE','SSC'],validators=[DataRequired()])
    tenmarks = StringField(label='10th marks',validators=[DataRequired()])
    twelveboard = SelectField(label='Class 12th Board',choices=['CBSE','ICSE','SSC'],validators=[DataRequired()])
    twelevemarks = StringField(label='12th marks',validators=[DataRequired()])
    course = SelectField(label='Course',choices=['BTECH','BCOM','BBA'],validators=[DataRequired()])
    branch = SelectField(label='BTECH Branch',choices=['CSE','MECH','EEE','ECE'],validators=[DataRequired()])
    dt = DateField('BIRTHDAY(Y/M/D)', format='%Y/%m/%d')
    next = SubmitField()





class StudentRegister(FlaskForm):
    name =  StringField(label='Name',validators=[DataRequired()])
    email = StringField(label='EMAIL',validators=[DataRequired(),Email(message='enter a valid email id ')])
    phone = StringField(label = 'number',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    another_password = PasswordField(label="Please retype the password",validators=[DataRequired()])
    submit = SubmitField()

class Login(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email(message='enter valid email id')])
    password = PasswordField(label='password',validators=[DataRequired()])
    submit = SubmitField()