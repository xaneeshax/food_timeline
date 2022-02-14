# Imports
from flask import Flask, request, jsonify, url_for, redirect
from flask_pymongo import PyMongo 
from flask_cors import CORS 
from bson.objectid import ObjectId
import datetime as dt
from dateutil import tz
import time
import cloudinary
import cloudinary.uploader
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os


# Create Flask App
app = Flask(__name__)

# Connecting the App to MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost/food'
mongo = PyMongo(app)


# Configure JWT
app.config["JWT_SECRET_KEY"] = 'dasfhalsfhljkafshd' #os.environ.get('JWT_SECRET')  # Change this!
print(app.config["JWT_SECRET_KEY"])
jwt = JWTManager(app)


# Connect Port 5000 with Port 3000
CORS(app)

# Different Collections being used in MongoDB
user_db = mongo.db.users 
post_db = mongo.db.posts
pics_db = mongo.db.pics


''' LOGIN '''

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)



''' HOME PAGE '''



# Home Route
@app.route('/')
def index():
    return 'API Running'



''' USER QUERIES '''



# Functionality to Create an Account or Login
@app.route('/users', methods=['POST'])
def create_user():
    id = user_db.insert_one({
        'name' : request.json['name'],
        'email' : request.json['email'],
        'password' : request.json['password']
    })
    
    print(str(id))
    return jsonify({'msg' : 'Create User Received'})



# Get all the users - not sure what this is for
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for doc in user_db.find():
        users.append({
            '_id' : str(ObjectId(doc['_id'])),
            'name' : doc['name'],
            'email' : doc['email'],
            'password' : doc['password']
        })
    return jsonify(users)



# Get a single user's information
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = user_db.find_one({"_id": ObjectId(id)})

    return jsonify({
        '_id' : str(ObjectId(user["_id"])),
        'name' : user['name'],
        'email' : user['email'],
        'password' : user['password']
    })



''' POST QUERIES '''



# Add a picture into your food timeline with Cloudinary
@app.route('/create_post', methods=['POST'])
def create_post():
    if 'profile_image' in request.files:  
        cloudinary.config(cloud_name = "aneeshasreerama", api_key=864559878353582, api_secret="FJXbQmOWw9Ixq3WuIfwzj4CKDQ0")
  
        upload_result = None
        if request.method == 'POST':
            file_to_upload = request.files['profile_image']
        
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, height=400, quality=100, width=400, crop="lpad")
            upload_result = dict(upload_result)

            username = request.form.get('username')
            secure_url = upload_result['secure_url']

            date = dt.datetime.now(dt.timezone.utc)
            utc_time = date.replace(tzinfo=dt.timezone.utc)
            utc_timestamp = utc_time.timestamp()

            info = time.strftime("%A %b %d, %Y", time.localtime(utc_timestamp))

            pic = pics_db.insert_one({
                'username' : username,
                'original_filename' : upload_result['original_filename'],
                'secure_url' : secure_url,
                'height' : upload_result['height'],
                'width' : upload_result['width']
            })

            post = post_db.insert_one({
                'username' : username,
                'item' : request.form.get('item'),
                'pic_url' : secure_url,
                'location' : request.form.get('location'),
                'timestamp' : info,
                'review' : request.form.get('review'),
                'rating' : request.form.get('rating'),
            })

            return redirect(f"http://localhost:3000")




# Get all the posts by a certain user
@app.route('/timeline/<username>', methods=['GET'])
def get_timeline(username):

    #user_id = user_db.find_one({"name": name})
    #user_id = str(ObjectId(user_id['_id']))

    posts = []
    for doc in post_db.find({'username' : username}):
        
        utc = doc['timestamp']

        posts.append({
            'post_id' : str(ObjectId(doc['_id'])),
            'item' : doc['item'],
            'pic_url' : doc['pic_url'],
            'location' : doc['location'],
            'timestamp' : utc,
            'review' : doc['review'],
            'rating' : doc['rating']
        })
    
    return jsonify(posts[::-1])



# Delete a post from the database
@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_db.delete_one({'_id' : ObjectId(post_id)})
    return jsonify({'msg' : 'Post Deleted'})



''' RUNNING THE APP '''



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='localhost')
