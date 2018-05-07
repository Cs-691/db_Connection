from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow








app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/test2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']='false'
db = SQLAlchemy(app)
ma = Marshmallow(app)
db.init_app(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=True)
    lastName = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    country = db.Column(db.String(120), unique=True)
    disabilities = db.Column(db.String(120), unique=True)
    conditions = db.Column(db.String(120), unique=True)

    def __init__(self, firstName, lastName,age,gender,email,password,country,disabilities,conditions):
        self.firstName = firstName
        self.lastName = lastName
        self.age=age
        self.gender=gender
        self.email=email
        self.password=password
        self.country=country
        self.disabilities=disabilities
        self.conditions=conditions


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('firstName', 'lastName','age')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/Adduser", methods=["POST"])
def add_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    age = request.json['age']
    gender = request.json['gender']
    email = request.json['email']
    password = request.json['password']
    country = request.json['country'] 
    disabilities = request.json['disabilities']
    conditions = request.json['conditions']
    
    new_user = User(firstName, lastName,age,gender,email,password,country,disabilities,conditions)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route('/')
def hello_world():
        return 'Hello, World12qw'


if __name__ == '__main__':
    app.run(debug=True)
