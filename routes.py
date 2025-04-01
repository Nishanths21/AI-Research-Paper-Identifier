from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from extensions import db
from utils.document_processor import process_document, calculate_similarity  # Ensure this is correct
from utils.email_sender import send_status_email
from models import Submission, Admin

main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/submit', methods=['GET', 'POST'])
def handle_submission():
    if request.method == 'POST':
        try:
            email = request.form['email']
            title = request.form['title']
            document = request.files['document']
            
            # Process document
            text, filename = process_document(document)
            
            # Calculate similarity
            max_score, matches = calculate_similarity(text)

            # Save submission
            submission = Submission(
                email=email,
                title=title,
                filename=filename,
                similarity_score=max_score,
                matches=matches,
                text_content=text
            )
            db.session.add(submission)
            db.session.commit()

            # Send confirmation email TO USER'S EMAIL
            send_status_email(
                action='submitted',
                user_email=email,
                details={
                    'score': max_score,
                    'matches': [m['title'] for m in matches]
                }
            )

            return render_template('submit_success.html', score=max_score)

        except Exception as e:
            current_app.logger.error(f"Submission error: {str(e)}")
            return "Internal Server Error", 500

    return render_template('user_submit.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin_user = Admin.query.filter_by(username=username).first()
        if admin_user and admin_user.password == password:  # Use hashed passwords in production!
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('admin_login.html')

@admin_bp.route('/dashboard')
def admin_dashboard():
    try:
        pending_submissions = Submission.query.filter_by(status='pending').all()
        return render_template('admin_dashboard.html', submissions=pending_submissions)
    except Exception as e:
        current_app.logger.error(f"Dashboard error: {str(e)}")
        return "Internal Server Error", 500

@admin_bp.route('/admin/action', methods=['POST'])
def handle_admin_action():
    try:
        data = request.get_json()
        submission_id = data['id']
        action_taken = data['action']

        submission = Submission.query.get(submission_id)
        if not submission:
            return jsonify({'status': 'error', 'message': 'Submission not found'}), 404
        
        submission.status = action_taken

        # Send email TO USER'S STORED EMAIL
        send_status_email(
            action=action_taken,
            user_email=submission.email,
            details={
                'score': submission.similarity_score,
                'matches': submission.matches or []
            }
        )

        db.session.commit()
        return jsonify({'status': 'success'})
        
    except Exception as e:
        current_app.logger.error(f"Admin action error: {str(e)}")
        return jsonify({'status': 'error'}), 500
