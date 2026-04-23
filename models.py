from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    USER = "user"
    COMPANY = "company"

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), nullable=False, default=UserRole.USER.value)

    participations = db.relationship('Participation', backref='user', lazy=True)
    favorite_events = db.relationship('FavoriteEvent', backref='user', lazy=True)
    favorite_vacancies = db.relationship('FavoriteVacancy', backref='user', lazy=True)

class RegisterValidation(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    mail: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: UserRole = Field(default=UserRole.USER)

class CompanyProfile(db.Model):
    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        unique=True
    )

    industry = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)

    user = db.relationship('User', backref='company_profile')

class Participation(db.Model):
    __tablename__ = 'participations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    event_title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    status = db.Column(db.String(20), default='registered')  # 'registered' или 'completed'
    achievement = db.Column(db.String(100), nullable=True)
    earned_points = db.Column(db.Integer, default=0)

    # НОВОЕ ПОЛЕ: Хранит имя файла сертификата
    certificate_file = db.Column(db.String(250), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FavoriteEvent(db.Model):
    __tablename__ = 'favorite_events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    event_title = db.Column(db.String(250), nullable=False)


class FavoriteVacancy(db.Model):
    __tablename__ = 'favorite_vacancies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vacancy_id = db.Column(db.Integer, nullable=False)
    vacancy_title = db.Column(db.String(250), nullable=False)
    hh_url = db.Column(db.String(500), nullable=True)

class InternalVacancy(db.Model):
    __tablename__ = 'internal_vacancies'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    salary_from = db.Column(db.Integer, nullable=True)
    salary_to = db.Column(db.Integer, nullable=True)
    experience = db.Column(db.String(100))
    schedule = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)