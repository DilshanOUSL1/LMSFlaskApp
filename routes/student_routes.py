from flask import Blueprint, render_template, flash, session, redirect, url_for
from models.models import db, User

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/<int:student_id>')
def view_student(student_id):
    # 1. Optional: Ensure user is logged in (or has a certain role)
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))
    
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    # 2. Fetch the student by ID
    student = User.query.get(student_id)
    if not student or student.role != 'student':
        flash("Student not found.", "danger")
        return redirect(url_for('dashboard'))  # or wherever you want to go

    # 3. Render a template that shows student info
    return render_template('view_student.html', student=student, user=user)
