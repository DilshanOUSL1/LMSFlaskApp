from flask import *
from extensions import bcrypt, SQLAlchemy

# Initialize Flask
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yoursecretkey'  # Needed for sessions, flash messages

# Initialize database
db = SQLAlchemy()

# Import models
from models.models import db, User, Course, Enrollment

# Initialize db with the Flask app
db.init_app(app)
bcrypt.init_app(app)
# Import & register auth blueprint
from routes.auth_routes import auth, bcrypt
bcrypt.init_app(app)
app.register_blueprint(auth, url_prefix='/auth')

# ------------------------
# Import & register course blueprint
from routes.course_routes import course_bp
app.register_blueprint(course_bp, url_prefix='/courses')
# ------------------------
# Import & register enrollment blueprint
from routes.enrollment_routes import enrollment_bp
app.register_blueprint(enrollment_bp, url_prefix='/enrollment')

from routes.student_routes import student_bp
app.register_blueprint(student_bp, url_prefix='/student')


# Create tables
with app.app_context():
    db.create_all()

# ---------------------------------------
# 1) ROOT ROUTE: Redirects to /dashboard
# ---------------------------------------
@app.route('/')
def home():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))
    # If logged in, send them to /dashboard
    return redirect(url_for('dashboard'))

# ---------------------------------------
# 2) DASHBOARD ROUTE: Role-based
# ---------------------------------------
@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    user_role = session.get('user_role', None)
    if not user_role:
        flash("You must be logged in first.", "danger")
        return redirect(url_for('auth.login'))

    # Fetch the logged-in user's details
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # -------------------------------------------------------
    #  Admin Dashboard
    # -------------------------------------------------------
    if user_role == 'admin':
        return render_template('admin_dashboard.html', user=user)

    # -------------------------------------------------------
    #  Instructor Dashboard
    # -------------------------------------------------------
    elif user_role == 'instructor':
        # Example: Show all students to the instructor
        students = User.query.filter_by(role='student').all()
        return render_template('instructor_dashboard.html', user=user, students=students)

    # -------------------------------------------------------
    #  Student Dashboard
    # -------------------------------------------------------
    else:
        # 1) Fetch enrollments for this student
        student_enrollments = Enrollment.query.filter_by(student_id=user_id).all()

        # 2) Build a list of the student's courses
        #    Suppose your Enrollment table has 'progress' or similar
        courses = []
        for e in student_enrollments:
            # e.course is possible if you set up a relationship (e.g., backref or relationship on Enrollment)
            # or you can do a separate query if you don't have that:
            # course = Course.query.get(e.course_id)
            # if course: ...
            # For demonstration, let's assume e.course works and e.progress exists:
            if e.course:
                courses.append({
                    'name': e.course.name,
                    'progress': e.progress  # or something similar
                })

        return render_template('student_dashboard.html', user=user, courses=courses)


# ---------------------------------------
# MAIN
# ---------------------------------------
if __name__ == '__main__':
    app.run(debug=True)