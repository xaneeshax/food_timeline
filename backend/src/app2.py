from flask import Flask, request, jsonify, url_for, redirect
from flask_pymongo import PyMongo 
from flask_cors import CORS 
from bson.objectid import ObjectId
import datetime as dt
from dateutil import tz
from PIL import Image
import numpy
import cv2
import io

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/food'
mongo = PyMongo(app)

CORS(app)

user_db = mongo.db.users 
post_db = mongo.db.posts
pics_db = mongo.db.pics

# Main Page
@app.route('/no')
def index():
    return '''
        <form method="POST" action="/create" enctype="multipart/form-data">
            <input type="text" name="username">
            <input type="file" name="profile_image">
            <input type="submit">
        </form>
    '''

@app.route('/resizeable', methods=['POST'])
def createless():
    if 'profile_image' in request.files:
        filestr1 = request.files['profile_image']
        filestr = request.files['profile_image'].read()

        
        
        #convert string data to numpy array
        npimg = numpy.fromstring(filestr, numpy.uint8)
        #print(type(npimg))
        
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        width = int(img.shape[1])
        height = int(img.shape[0])
        
        im = Image.new("RGB", (100, 100))
        b = io.BytesIO()
        im.save(b, "JPEG")
        im.show()
        # Save to MongoDB
        mongo.save_file(filestr1.filename, im)
        pics_db.insert_one({'username' : request.form.get('username'), 
        'profile_image_name' : 'an_img.jpg'})
        return f'width: {width}, height: {height}'


@app.route('/create', methods=['POST'])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        pics_db.insert_one({'username' : request.form.get('username'), 
        'profile_image_name' : profile_image.filename})
    return 'done!'

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/resize/<username>', methods=['GET'])
def resize(username):
    user = pics_db.find_one_or_404({'username' : username})
    pic_url = f"http://localhost:5000/file/{user['profile_image_name']}"
    im = mongo.send_file(user['profile_image_name'])
    print(type(im))
    return im
    


@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = pics_db.find_one_or_404({'username' : username})
    return f'''
        <h1>{username}</h1>
        <img src="http://localhost:5000/files/{user['profile_image_name']}" width="300" height="300">

    '''

# {url_for('file', filename=user['profile_image_name'])}




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



# Get all the Users - not sure what this is for
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
@app.route('/')
def index():
    return 'API Running'

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



# Create a post given a user
@app.route('/posts', methods=['POST'])
def create_post():
    
    date = dt.datetime.now(dt.timezone.utc)
    utc_time = date.replace(tzinfo=dt.timezone.utc)
    utc_timestamp = utc_time.timestamp()

    post = post_db.insert_one({
        'user_id' : request.json['user_id'],
        'location' : request.json['location'],
        'timestamp' : utc_timestamp,
        'review' : request.json['review'],
        'rating' : request.json['rating']
    })

    print(str(post))
    return jsonify({'msg' : 'Create Post Received'})



# Create a post given a user
@app.route('/foodies', methods=['POST'])
def foodies():

    profile_image = request.json['pic']
    mongo.save_file('image_id', profile_image)
    pics_db.insert_one({
        'username' : request.form.get('username'), 
        'post_image' : 'image_id'
    })
    
    date = dt.datetime.now(dt.timezone.utc)
    utc_time = date.replace(tzinfo=dt.timezone.utc)
    utc_timestamp = utc_time.timestamp()

    post = post_db.insert_one({
        'user_id' : request.json['user_id'],
        'location' : request.json['location'],
        'timestamp' : utc_timestamp,
        'review' : request.json['review'],
        'rating' : request.json['rating'],
        'pic' : request.json['pic']
    })

    print(str(post))
    return jsonify({'msg' : 'Create Post Received'})



# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = []
    for doc in post_db.find():
        posts.append({
            'post_id' : str(ObjectId(doc['_id'])),
            'user_id' : doc['user_id'],
            'location' : doc['location'],
            'timestamp' : doc['timestamp'],
            'review' : doc['review'],
            'rating' : doc['rating']
        })
    return jsonify(posts)


# Create a post given a user
@app.route('/posts', methods=['POST'])
def create_post():
    
    date = dt.datetime.now(dt.timezone.utc)
    utc_time = date.replace(tzinfo=dt.timezone.utc)
    utc_timestamp = utc_time.timestamp()

    post = post_db.insert_one({
        'user_id' : request.json['user_id'],
        'location' : request.json['location'],
        'timestamp' : utc_timestamp,
        'review' : request.json['review'],
        'rating' : request.json['rating']
    })

    print(str(post))
    return jsonify({'msg' : 'Create Post Received'})




# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = []
    for doc in post_db.find():
        posts.append({
            'post_id' : str(ObjectId(doc['_id'])),
            'user_id' : doc['user_id'],
            'location' : doc['location'],
            'timestamp' : doc['timestamp'],
            'review' : doc['review'],
            'rating' : doc['rating']
        })
    return jsonify(posts[::-1])


# Get all the posts by a certain user
@app.route('/posts/<name>', methods=['GET'])
def get_user_posts(name):

    user_id = user_db.find_one({"name": name})
    user_id = str(ObjectId(user_id['_id']))

    posts = []
    for doc in post_db.find({'user_id' : user_id}):
        #from_zone = tz.tzutc()
        #to_zone = tz.tzlocal()
        utc = doc['timestamp']

        # datetime objects are 'naive' by default
        #utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        #converted_date = utc.astimezone(to_zone)

        posts.append({
            'post_id' : str(ObjectId(doc['_id'])),
            'user_id' : doc['user_id'],
            'location' : doc['location'],
            'timestamp' : utc,
            'review' : doc['review'],
            'rating' : doc['rating']
        })
    
    return jsonify(posts)


# Create a post given a user
@app.route('/foodies', methods=['POST'])
def foodies():

    profile_image = request.json['pic']
    mongo.save_file('image_id', profile_image)
    pics_db.insert_one({
        'username' : request.form.get('username'), 
        'post_image' : 'image_id'
    })
    
    date = dt.datetime.now(dt.timezone.utc)
    utc_time = date.replace(tzinfo=dt.timezone.utc)
    utc_timestamp = utc_time.timestamp()

    post = post_db.insert_one({
        'user_id' : request.json['user_id'],
        'location' : request.json['location'],
        'timestamp' : utc_timestamp,
        'review' : request.json['review'],
        'rating' : request.json['rating'],
        'pic' : request.json['pic']
    })

    print(str(post))
    return jsonify({'msg' : 'Create Post Received'})



# Get all the posts by a certain user
@app.route('/posts/<name>', methods=['GET'])
def get_user_posts(name):

    #user_id = ''
    #for doc in user_db.find_one({"name": name}):
    #    print(doc)
    #    user_id = str(ObjectId(doc['_id'])),
    user_id = user_db.find_one({"name": name})
    user_id = str(ObjectId(user_id['_id']))

    posts = []
    for doc in post_db.find({'user_id' : user_id}):
        #from_zone = tz.tzutc()
        #to_zone = tz.tzlocal()
        utc = doc['timestamp']

        # datetime objects are 'naive' by default
        #utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        #converted_date = utc.astimezone(to_zone)

        posts.append({
            'post_id' : str(ObjectId(doc['_id'])),
            'user_id' : doc['user_id'],
            'location' : doc['location'],
            'timestamp' : utc,
            'review' : doc['review'],
            'rating' : doc['rating']
        })
    
    return jsonify(posts)



# Delete a post from the database
@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_db.delete_one({'_id' : ObjectId(post_id)})
    return jsonify({'msg' : 'Post Deleted'})


''' IMAGES WITH MONGO DB '''


# Add a picture into your food timeline
@app.route('/create', methods=['POST'])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        pics_db.insert_one({'username' : request.form.get('username'), 
        'profile_image_name' : profile_image.filename})
    return 'done!'



# Add a picture into your food timeline with Cloudinary
@app.route('/cloud_upload', methods=['POST'])
def cloud_upload():
    if 'profile_image' in request.files:  
        cloudinary.config(cloud_name = "aneeshasreerama", api_key=864559878353582, api_secret="FJXbQmOWw9Ixq3WuIfwzj4CKDQ0")
  
        upload_result = None
        if request.method == 'POST':
            file_to_upload = request.files['profile_image']
        
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload, height=400, quality=80, width=400, crop="lpad")
            upload_result = dict(upload_result)
            username = request.form.get('username')

            pic = pics_db.insert_one({
                'username' : username,
                'original_filename' : upload_result['original_filename'],
                'secure_url' : upload_result['secure_url'],
                'height' : upload_result['height'],
                'width' : upload_result['width']
            })

            return redirect(f"/posts/{username}")

            # dict_keys(['asset_id', 'public_id', 'version', 'version_id', 'signature', 
            # 'width', 'height', 'format', 'resource_type', 
            # 'created_at', 'tags', 'bytes', 'type', 'etag',
            # 'placeholder', 'url', 'secure_url', 'access_mode', 'original_filename', 'api_key'])




# Get a file from MongoDB
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)



# Return a pic from the user
@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = pics_db.find_one_or_404({'username' : username})
    return f'''
        <h1>{username}</h1>
        <img src="http://localhost:5000/files/{user['profile_image_name']}" width="300" height="300">

    '''



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='localhost')