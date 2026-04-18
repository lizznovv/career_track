from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)

    participations = db.relationship('Participation', backref='user', lazy=True)
    favorite_events = db.relationship('FavoriteEvent', backref='user', lazy=True)
    favorite_vacancies = db.relationship('FavoriteVacancy', backref='user', lazy=True)


class Participation(db.Model):
    __tablename__ = 'participations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    event_title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    # НОВЫЕ ПОЛЯ ДЛЯ ГЕЙМИФИКАЦИИ
    status = db.Column(db.String(20), default='registered')  # 'registered' или 'completed'
    achievement = db.Column(db.String(100), nullable=True)  # Победитель, Участник и тд
    earned_points = db.Column(db.Integer, default=0)  # Сколько баллов принесло именно это событие

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