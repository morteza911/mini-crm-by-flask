from crm import db 
import datetime
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy



from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    family = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)  
    family = db.Column(db.String(30), nullable=True) 
    phone_number = db.Column(db.String(15), nullable=True)  
    phone_number_two = db.Column(db.String(15), nullable=True)  
    phone_number_three = db.Column(db.String(15), nullable=True)  
    email = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    negotiations = db.relationship('Negotiation', backref='customer', lazy=True)  

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    negotiations = db.relationship('Negotiation', backref='stage', lazy=True)  

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False) 
    description = db.Column(db.String(500), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(230), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)  
    phone_number_two = db.Column(db.String(15), nullable=True)  
    phone_number_three = db.Column(db.String(15), nullable=True)  
    fax = db.Column(db.String(15), nullable=True)  
    website = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    negotiations = db.relationship('Negotiation', backref='company', lazy=True) 

class Negotiation(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(30), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'), nullable=True)  # تغییر نام از Company به company_id
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'), nullable=True)  # تغییر نام از Customer به customer_id
    amount = db.Column(db.Integer, nullable=True)
    done = db.Column(db.Boolean, nullable=False, default=False)  # حذف done تکراری
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id', ondelete='CASCADE'), nullable=True)  # تغییر نام از stage به stage_id
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # تغییر نام از data به date
    priority = db.Column(db.Integer, nullable=True)  # حذف primary_key=True
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=True)  # تغییر نام و حذف primary_key=True
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # تغییر نام از user به user_id

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    negotiation_id = db.Column(db.Integer, db.ForeignKey('negotiation.id', ondelete='CASCADE'), nullable=False)  # اصلاح به negotiation_id
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete='CASCADE'), nullable=False)
    note = db.Column(db.String(255), nullable=False)  # تغییر اندازه از 30 به 255
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # تغییر نام از User به user_id
    date_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # اصلاح به date_registration و تغییر به DateTime
    negotiation = db.relationship('Negotiation', backref='records', lazy=True)
    activity = db.relationship('Activity', backref='records', lazy=True)
    
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.DateTime, nullable=False)  # تغییر نام به visit_date و تغییر به DateTime
    negotiation_id = db.Column(db.Integer, db.ForeignKey('negotiation.id', ondelete='CASCADE'), nullable=False)  # اضافه کردن negotiation_id به جای backref اشتباه
