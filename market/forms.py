from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User
from wtforms.fields import DateField,DateTimeField,SelectField,choices
class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address Already Exists!! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(),DataRequired()])
    password1 = PasswordField(label="Password:",validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2,max=30),DataRequired()])
    password = PasswordField(label="Password:",validators=[Length(min=6),DataRequired()])
    submit = SubmitField(label='Sign In')

class CourseForm(FlaskForm):
    batch = SelectField(label='Batch No:',choices=[('Batch1','Batch1'),('Batch2','Batch2')])
    regulartype = SelectField(label='Course Type:',choices=[('Regular','Regular'),('IrRegular','IrRegular')])
    cname = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('Python', 'Python'),('C Language','C language')])
    submit = SubmitField(label='Register Course')
    
    

