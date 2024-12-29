from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize the database object

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, instructor, or student
    student_id = db.Column(db.String(20), unique=True, nullable=True)
    index_number = db.Column(db.Integer, nullable=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    def __repr__(self):
        return f"<Enrollment student_id={self.student_id} course_id={self.course_id}>"
