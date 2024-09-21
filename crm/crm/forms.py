from flask_wtf import FlaskForm
from wtforms import PasswordField,BooleanField
from wtforms import StringField, IntegerField, TextAreaField,SelectField, SubmitField, DateTimeField
from wtforms.validators import  length ,equal_to, Length
from khayyam import JalaliDatetime
from wtforms.validators import   Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import datetime
from crm.models import Company, Customer, Stage, Campaign, Negotiation, Activity  
from wtforms import StringField, IntegerField
from wtforms.validators import   Email, EqualTo, ValidationError
from crm.models import User
from wtforms.validators import DataRequired

# در بالای فایل forms.py



class CustomerForm(FlaskForm):
    name = StringField('username', validators=[DataRequired(),length(min=4,max=30)])
    family = StringField('family')
    phone_number = StringField('phone_number')
    phone_number_two = StringField('phone_number_two')
    phone_number_three = StringField('phone_number_three' )
    email =StringField('email')
    

class ActivityForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(),length(min=3,max=30)])


class StageForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(),length(min=3,max=30)])


class CampaignForm(FlaskForm):
    name = StringField('username', validators=[DataRequired(),length(min=3,max=500)])
    description = StringField('phone_number_two')


class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=4, max=30)])
    address = StringField('Address')
    phone_number = StringField('Phone Number')
    phone_number_two = StringField('Phone Number Two')
    phone_number_three = StringField('Phone Number Three')
    fax = StringField('Fax')
    website = StringField('Website')
    email = StringField('Email' )
    submit = SubmitField('Submit')



class NegotiationForm(FlaskForm):

    topic = StringField('Topic', validators=[DataRequired(), Length(min=3, max=30)])
    # فیلد انتخابی برای شرکت
    company_id = QuerySelectField('Company', query_factory=lambda: Company.query.all(), get_label='name', allow_blank=True, blank_text='-- بدون شرکت --', validators=[Optional()])
    # فیلد انتخابی برای مشتری
    customer_id = QuerySelectField('Customer', query_factory=lambda: Customer.query.all(), get_label='name', allow_blank=True, blank_text='-- بدون مشتری --', validators=[Optional()])
    # فیلد عددی برای مبلغ
    amount = IntegerField('Amount', validators=[Optional(), NumberRange(min=0)])
    # فیلد انتخابی برای وضعیت انجام شده
    done = BooleanField('Done', default=False)
    # فیلد انتخابی برای مرحله
    stage_id = QuerySelectField('Stage', query_factory=lambda: Stage.query.all(), allow_blank=False, get_label='name', validators=[DataRequired()]) 
    # فیلد عددی برای اولویت
    priority = IntegerField('Priority', validators=[Optional(), NumberRange(min=0, max=100)])
    # فیلد انتخابی برای کمپین
    campaign_id = QuerySelectField('Campaign', query_factory=lambda: Campaign.query.all(), allow_blank=True, blank_text='-- بدون کمپین --', get_label='name', validators=[Optional()])


class DeleteForm(FlaskForm):
    submit = SubmitField('حذف')
    



class RecordForm(FlaskForm):
    negotiation_id = QuerySelectField('Negotiation', query_factory=lambda: Negotiation.query.all(), get_label='topic', validators=[DataRequired()])
    activity_id = QuerySelectField('Activity', query_factory=lambda: Activity.query.all(), get_label='name', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()], render_kw={"maxlength": 255})

class Record_id_Form(FlaskForm):
    activity_id = QuerySelectField('Activity', query_factory=lambda: Activity.query.all(), get_label='name', validators=[DataRequired()])
    note = TextAreaField('Note', validators=[DataRequired()], render_kw={"maxlength": 255})


from flask_wtf import FlaskForm
from wtforms import DateTimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms_components import DateField

class VisitForm(FlaskForm):
    visit_date = DateField('Visit Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    
    

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    family = StringField('Family', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Custom validator to check if email is already registered
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
