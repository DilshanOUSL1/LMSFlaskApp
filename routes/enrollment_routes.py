from flask import *
from models.models import *
from extensions import db
from flask import Blueprint

enrollment_bp = Blueprint('enrollment_bp', __name__)
@enrollment_bp.route('/view_courses')
def view_courses():
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))
    
    # Allow only admin or instructor
    user_role = session.get('user_role', None)
    if user_role not in ['admin', 'instructor']:
        flash("Access denied. Only admins and instructors can view this page.", "danger")
        return redirect(url_for('dashboard'))

    # Fetch all courses
    available_courses = Course.query.all()
    student_id = request.args.get('student_id', type=int)
    return render_template('view_courses.html', courses=available_courses, student_id=student_id)

@enrollment_bp.route('/enroll/<int:course_id>', methods=['GET', 'POST'])
def enroll(course_id):
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))
    
    user_role = session.get('user_role', None)
    if user_role != 'student':
        flash("Only students can enroll in courses.", "danger")
        return redirect(url_for('dashboard'))
    
    student_id = session['user_id']

    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing_enrollment:
        flash("The Student is already enrolled in this course.", "info")
        return redirect(url_for('enrollment_bp.view_courses'))

    # Otherwise, create a new enrollment
    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()

    flash("Enrollment successful!", "success")
    return redirect(url_for('enrollment_bp.view_courses'))



