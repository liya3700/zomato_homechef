import os
from flask import current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from app.models import Location, User, db


def init_routes(app):
    
    @app.route('/')
    def initial():
        return redirect(url_for('login'))
    
    
    @app.route('/home')
    def home():
        profile_pic = request.args.get('profile_pic', "/static/images/default.jpg")
        return render_template('home.html', profile_pic=profile_pic)
    
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']        
            user = User.query.filter_by(email=email, password=password).first()
            print("MyPrint:::",user)

            if user:
                session['user_id'] = user.id
                if user.isHomeChef:
                    return redirect(url_for('hc_home', profile_pic=user.profile_pic))
                else:
                    return redirect(url_for('home', profile_pic=user.profile_pic))
            else:
                flash("Invalid email or password", "danger")

        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            isHomeChefValue = request.form.get('isHomeChef')
            if isHomeChefValue: 
                print("isHomeChef: Yes")
                isHomeChef = True
                
            else:
                print("isHomeChef: No")
                isHomeChef = False
            
            profile_pics = request.files.getlist('profile-pic')

            saved_files = []
            fn = ''
            for image in profile_pics:
                if image.filename:
                    filename = secure_filename(image.filename)
                    fn = filename
                    print("FileName:", filename)
                    
                    upload_folder = current_app.config.get('UPLOAD_FOLDER_PROFILE_PIC', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    file_path = os.path.join(upload_folder, filename)
                    image.save(file_path)
                    saved_files.append(filename)

            print("Saved Files:", saved_files)
                
            location_id = request.form.get('location')
            print("Location", location_id)

            user = User(username=username, email=email, password=password, isHomeChef=isHomeChef, profile_pic=fn, location_id=location_id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        
        locations = Location.query.all()
        return render_template('signup.html', locations=locations)