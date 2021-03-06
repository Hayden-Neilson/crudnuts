# add attribute for loggedIn: NOT_LOGGED_IN
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env= Env()
env.read_env()
DATABASE_URL = env('DATABASE_URL')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL


db = SQLAlchemy(app)
ma = Marshmallow(app)

## USER CLASS ##

class User(db.Model):
     __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, authentication):
        self.email = email
        self.password = password
        self.authentication = authentication

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'authentication')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

## PRODUCT CLASS ##

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(500))
    description = db.Column(db.String(300))
    review = db.Column(db.String(300))
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    available = db.Column(db.Integer)

    def __init__(self, name, image, description, review, category, quantity, available):
        self.name = name
        self.image = image
        self.description = description
        self.review = review
        self.category = category
        self.quantity = quantity
        self.available = available

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'image', 'description', 'review', 'category', 'quantity', 'available')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


## USER LOGIC/ENDPOINTS ##
# route("/logged-in")
# query for user, check logged in status, return user
@app.route("/login", methods=["POST"])
def login():
    email = request.json["user_email"]
    password = request.json["password"]

    user = User.query.filter_by(user_email = email).first()
    print(user)
    if user:
        if user.user_password == password:
            user.logged_in = "LOGGED_IN"
            return user_schema.jsonify(user)
        else:
            return jsonify("Invalid Credentials")
    else:
        return jsonify("Invalid User")

def is_active(self):
        """True, as all users are active."""
        return True

def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@login_manager.user_loader
def user_loader(user_id):

    return User.query.get(user_id)

@bull.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("bull.reports"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")


@app.route('/auth/<id>', methods=["DELETE"])
def delete_user(id):
    record = User.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Deleted.')



@app.route("/", methods=["GET"])
def home():
    return "<h1> Flask Backend </h1>"

## PRODUCT LOGIC/ ENDPOINTS ##

#GET
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>', methods=['GET'])
def get_product():
    product = Product.query.get(id)

    result = product_schema.dump(product)
    return jsonify(result)

#POST
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json['name']
    image = request.json['image']
    description = request.json['description']
    review = request.json['review']
    category = request.json['category']
    quantity = request.json['quantity']
    available = request.json['available']

    new_product = Product(name, image, description, review, category, quantity, available)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)
    return product_schema.jsonify(product)

#PUT / PATCH
@app.route("/product/<id>", methods=["PATCH"])
def update_product(id):
    product = Product.query.get(id)

    new_name = request.json['name']
    new_image = request.json['image']
    new_description = request.json['description']
    new_review = request.json['review']
    new_category = request.json['category']
    new_quantity = request.json['quantity']
    new_available = request.json['available']

    product.name = new_name
    product.image = new_image
    product.description = new_description
    product.review = new_review
    product.category = new_category
    product.quantity = new_quantity
    product.available = new_available

    db.session.commit()
    return product_schema.jsonify(product)

#DELETE
@app.route('/product/<id>', methods=["DELETE"])
def delete_product(id):
    record = Product.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Deleted.')

if __name__ == "__main__":
    app.debug = True
    app.run()