import os
from app.routes import init_routes
from flask import Flask, send_from_directory
from app.database import db
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['UPLOAD_FOLDER'] = 'app/uploads/images'
    app.config['UPLOAD_FOLDER_PROFILE_PIC'] = 'app/uploads/profile_pics'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'zomatoDb.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    
    db.init_app(app)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_routes(app)

    with app.app_context():

        db.create_all()
        
        @app.route('/uploads/images/<path:filename>')
        def download_file(filename):
            return send_from_directory('uploads/images', filename)
        
        @app.route('/uploads/profile_pics/<path:filename>')
        def get_profile_pic_url(filename):
            return send_from_directory('uploads/profile_pics', filename)

    return app