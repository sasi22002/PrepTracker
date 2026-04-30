from datetime import datetime
from extensions import db

class Company(db.Model):
    __tablename__ = 'company_data'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    
    # Relationships
    interviews = db.relationship('Interview', backref='company', lazy=True)
    questions = db.relationship('QuestionAnswer', backref='company_question', lazy=True)

class Interview(db.Model):
    __tablename__ = 'interview_master'
    
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    company_name_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)
    status = db.Column(db.String(50))  # e.g., 'Did well', 'Not well'
    state = db.Column(db.String(100))  # e.g., 'Moved to next', 'Failed', etc.
    is_deleted = db.Column(db.Boolean, default=False)
    is_attended = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('QuestionAnswer', backref='interview', lazy=True, foreign_keys='QuestionAnswer.interview_id')

class QuestionAnswer(db.Model):
    __tablename__ = 'question_master'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20))  # Python, Django, Cloud, General, Others, Database, Pandas
    interview_id = db.Column(db.Integer, db.ForeignKey('interview_master.sno'), nullable=False)
    company_question_id = db.Column(db.Integer, db.ForeignKey('company_data.id'), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StudyMaterial(db.Model):
    __tablename__ = 'preparation_master'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    belongs_to = db.Column(db.String(20))
    repeat_count = db.Column(db.Integer, default=0)
    question_type = db.Column(db.String(20), default='theory')  # 'coding' or 'theory'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
