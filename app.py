from flask import Flask
from config import Config
from extensions import db, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        from routes import main_bp, admin_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(admin_bp)
        
        # Create tables if not exists
        db.create_all()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4449, debug=True)
