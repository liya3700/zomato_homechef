import os
from flask import current_app, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from app.models import Items, Location, User, db


def init_routes(app):
    
    @app.route('/')
    def initial():
        return redirect(url_for('login'))
    
    
    @app.route('/home')
    def home():
        return render_template('home.html', profile_pic=session['profile_pic'])
    
    @app.route('/hc_home')
    def hc_home():
        return render_template('hc_home.html', profile_pic=session['profile_pic'])
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']        
            user = User.query.filter_by(email=email, password=password).first()
            print("MyPrint:::",user)

            if user:
                session['user_id'] = user.id
                session['profile_pic'] = user.profile_pic
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
    
    
    @app.route('/addItem', methods=['GET', 'POST'])
    def addItem():
        if 'user_id' in session:
            print("Logged In...........")
        else:
            print("Not Logged In................")
        if request.method == 'POST':
            if 'user_id' in session:
                item_name = request.form['item-name']
                desc = request.form['desc']
                price = request.form['price']
                item_images = request.files.getlist('item-images')
                fileName = ''
                for image in item_images:
                    if image.filename != '':
                        filename = secure_filename(image.filename)
                        fileName = filename
                        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                        
                item = Items(name=item_name,
                                    desc=desc,
                                    price=price,
                                    image=fileName,
                                    user_id=session['user_id']
                                    )
                    
                try:
                    db.session.add(item)
                    db.session.commit()
                    flash('Product added successfully!', 'success')
                    # return redirect(url_for('sell_product.go_to_home'))
                except Exception as e:
                    db.session.rollback()
                    flash('Product not added!', 'failed')
                finally:
                    db.session.close()
            else:
                print('User not logged in....')
    
        else:
            flash('Please fill all the required fields and add at least one image.', 'error')

        return render_template('addItem.html')
    
    
    @app.route('/get_all_items')
    def getAllItems():
        items = Items.query.all()
        items_dict = [item.to_dict() for item in items]
        response = jsonify({'status':'success','msg': 'success!!', 'data': items_dict})
        return response
    

    @app.route('/get_all_chefs')
    def getAllChefs():
        chefs = User.query.filter_by(isHomeChef=True)
        chefs_dict = [chef.to_dict() for chef in chefs]
        response = jsonify({'status':'success','msg': 'success!!', 'data': chefs_dict})
        return response

    @app.route('/get_location/<int:location_id>', methods=['GET'])
    def getLocationFromId(location_id):
        location = Location.query.get(location_id)
        if location:
            return jsonify({"location_name": location.name})
        return jsonify({"error": "Location not found"}), 404
    
    @app.route('/getItemsByChefId/<int:id>', methods=['GET'])
    def getItemsByChefId(id):
        chef_items = Items.query.filter(Items.user_id==id).all()
        chef = User.query.get(id)
        me = User.query.get(session['user_id'])
        return render_template('chef_detail_page.html', datas=chef_items, chef_data=chef, profile_pic = me.profile_pic)
    

    @app.route('/delete_item/<int:item_id>', methods=['POST', 'GET'])
    def delete(item_id):
        item = Items.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'Item deleted successfully'}, 200
        else:
            return {'message': 'Item not found'}, 404
        
    @app.route('/complete_order<int:item_id>', methods=['GET', 'POST'])
    def complete_order(item_id):
        item = Items.query.get(item_id)
        return render_template('complete_order.html', food=item)