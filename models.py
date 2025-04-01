from extensions import db

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    similarity_score = db.Column(db.Float)
    matches = db.Column(db.JSON)  # Store matching papers as JSON
    text_content = db.Column(db.Text)  # Full text for future comparisons
    status = db.Column(db.String(20), default='pending')

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords in production
