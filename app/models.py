from app.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    isHomeChef = db.Column(db.Boolean, default=False)
    profile_pic = db.Column(db.String(100), nullable=False, unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', name='fk_location_id'), nullable=False)
    location = db.relationship('Location', backref=db.backref('user', lazy=True))
    
    def to_dict(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile_pic': self.profile_pic,
            'isHomeChef': self.isHomeChef,
            'location': self.location.name
        }
        
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name
        }
        
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    desc = db.Column(db.String(100), nullable=False, unique=True)
    image = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.String(10), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))
    
    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'image': self.image,
            'price': self.price,
            'user_name': self.user.username
        }