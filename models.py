from flask_sqlalchemy import SQLAlchemy

# from app import db 
db = SQLAlchemy()


class Committee(db.Model):
    __tablename__ = 'committee'
    cid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sc = db.Column(db.Integer, nullable=False)
    faculty_incharge = db.Column(db.String)
    faculty_email = db.Column(db.String)
    student_incharge = db.Column(db.String)
    contact = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    domain = db.Column(db.String)
    about = db.Column(db.String)
    strength = db.Column(db.Integer)
    website = db.Column(db.String, nullable=False)
    socials = db.Column(db.String, nullable=False)


class MainEvent(db.Model):
    __tablename__ = 'main_event'
    eid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    cid  = db.Column(db.Integer, db.ForeignKey("committee.cid"), nullable=False)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    event_website = db.Column(db.String)
    event_socials = db.Column(db.String)
    image = db.Column(db.String, nullable=False)


class SubEvent(db.Model):
    __tablename__='sub_event'
    seid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    eid  = db.Column(db.Integer, db.ForeignKey("main_event.eid"), nullable=False)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=True)
    end_time = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    link = db.Column(db.String)

class Sponsors(db.Model):
    __tablename__='sponsor'
    sid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    eid  = db.Column(db.Integer, db.ForeignKey("main_event.eid"), nullable=False)
    image = db.Column(db.String, nullable=False)

class Newsletter(db.Model):
    __tablename__='newsletter'
    nid = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String,  unique=True)