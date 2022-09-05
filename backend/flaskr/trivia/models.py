from flask_sqlalchemy import SQLAlchemy

from flaskr.config import settings

database_name = settings.DB_NAME
database_path = settings.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    questions = db.relationship('Question', backref='category')

    def __init__(self, name):
        self.type = name

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }


"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    difficulty = db.Column(db.Integer)

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.type,
            'difficulty': self.difficulty
            }

